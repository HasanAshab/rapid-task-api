from ranker.common.gpt import GroqGPTCompletion
from .models import Difficulty


class DifficultyGPTCompletion(GroqGPTCompletion):
    PROMPT = """Suggest difficulty for the challenge.
    You will be provided available difficulties (from easiest to hardest),
    info of the user, previous challenges with their
    relevant difficulty and the challenge.
    Note: response should be only the difficulty name,
    no extra spaces and talks.
    """

    def clean_result(self, result):
        return result.strip()

    def is_valid_result(self, result):
        return Difficulty.objects.exists(slug=result)
