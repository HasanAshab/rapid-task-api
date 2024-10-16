from django.conf import settings
from ranker.common.gpt import GeminiGPTCompletion


class DifficultyGPTCompletion(GeminiGPTCompletion):
    system_instruction = """
    You are a difficulty detector.

    Note: response should be only the difficulty score (in Float).
    no extra spaces and talks.

    Suggest difficulty for the challenge.
    You will be provided score range of difficulty,
    info of the user, previously completed challenges with their
    difficulty score and the challenge thats difficulty to be detected.

    example response: 5.203
    """

    fallback_result = 2

    def clean_result(self, result):
        return round(
            float(result.strip()) - settings.DIFFICULTY_SUGGESTION_THRESHOLD
        )

    def is_valid_result(self, result):
        return isinstance(result, int)
