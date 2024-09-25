from ranker.common.gpt import GroqGPTCompletion
from .models import Difficulty


class DifficultyGPTCompletion(GroqGPTCompletion):
    PROMPT = """Suggest difficulty for the challenge.
    You will be provided available difficulties (from easiest to hardest),
    info of the user, previously completed challenges with their
    relevant difficulty and the challenge thats difficulty to be detected.

    Note: response should be only the difficulty name,
    no extra spaces and talks. Give the difficulty
    easier than users previous challenge as the user grows
    by completing those before
    """

    def clean_result(self, result):
        return result.strip()

    def is_valid_result(self, result):
        return Difficulty.objects.exists(slug=result)
