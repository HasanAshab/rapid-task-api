from ranker.common.gpt import GroqGPTCompletion
from .models import Difficulty


class DifficultyGPTCompletion(GroqGPTCompletion):
    system_message = """
    Note: response should be only the difficulty name,
    no extra spaces and talks.

    Suggest difficulty for the challenge.
    You will be provided available difficulties (from easiest to hardest),
    info of the user, previously completed challenges with their
    relevant difficulty and the challenge thats difficulty to be detected.
    """

    def clean_result(self, result):
        return result.strip()

    def is_valid_result(self, result):
        return Difficulty.objects.filter(slug=result).exists()
