import json
from pydantic import BaseModel, ValidationError
from abc import abstractmethod
from django.conf import settings


class BaseGPTCompletion:
    MAX_ATTEMPTS = 1
    API_KEY = None
    fallback_result = None

    def __init__(self, message):
        self._message = message
        self._client = self.get_client()

    @property
    @abstractmethod
    def system_instruction(self):
        pass

    @abstractmethod
    def get_client(self):
        pass

    def get_api_key(self):
        if not self.API_KEY:
            raise Exception("API key is not set")
        return self.API_KEY

    def get_fallback_result(self):
        return self.fallback_result

    def clean_result(self, result):
        return result

    def is_valid_result(self, result):
        return True

    def create(self, max_attempts=None):
        max_attempts = max_attempts or self.MAX_ATTEMPTS
        for _ in range(max_attempts):
            if result := self.generate():
                return result
        return self.get_fallback_result()

    @abstractmethod
    def get_result(self):
        pass

    def generate(self):
        dirty_result = self.get_result()
        result = self.clean_result(dirty_result)
        if self.is_valid_result(result):
            return result


class JSONGPTCompletionMixin:
    @property
    @abstractmethod
    def response_schema(self) -> BaseModel:
        pass

    def clean_result(self, result):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return result

    def is_valid_result(self, result):
        try:
            self.response_schema.model_validate(result)
            return True
        except ValidationError:
            return False


class GroqGPTCompletion(BaseGPTCompletion):
    MODEL = "llama3-8b-8192"

    def get_api_key(self):
        return settings.GROQ_API_KEY

    def get_client(self):
        from groq import Groq

        return Groq(api_key=self.get_api_key())

    def get_result(self):
        completion = self._client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": self.system_instruction},
                {"role": "user", "content": self._message},
            ],
        )
        return completion.choices[0].message.content


class GeminiGPTCompletion(BaseGPTCompletion):
    MODEL = "gemini-1.5-pro"

    def get_api_key(self):
        return settings.GEMINI_API_KEY

    def get_client(self):
        import google.generativeai as genai

        genai.configure(api_key=self.get_api_key())
        return genai.GenerativeModel(
            model_name=self.MODEL,
            system_instruction=self.system_instruction,
        )

    def get_result(self):
        content = self._client.generate_content(self._message)
        return content.text


class GeminiJSONGPTCompletion(JSONGPTCompletionMixin, GeminiGPTCompletion):
    def get_result(self):
        import google.generativeai as genai

        content = self._client.generate_content(
            self._message,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=self.response_schema,
            ),
        )
        return content.text
