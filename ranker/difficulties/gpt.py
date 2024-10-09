from ranker.common.gpt import GeminiGPTCompletion
from .models import Difficulty


class DifficultyGPTCompletion(GeminiGPTCompletion):
    system_instruction = """
    You are a difficulty detector.

    Note: response should be only the difficulty name,
    no extra spaces and talks.

    Suggest difficulty for the challenge.
    You will be provided available difficulties (from easiest to hardest),
    info of the user, previously completed challenges with their
    relevant difficulty and the challenge thats difficulty to be detected.
    """

    def get_fallback_result(self):
        return Difficulty.objects.values_list("slug", flat=True).first()

    def clean_result(self, result):
        return result.strip().lower()

    def is_valid_result(self, result):
        return Difficulty.objects.filter(slug=result).exists()
