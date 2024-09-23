import re
import json
from ranker.common.gpt import GroqGPTCompletion


class ChallengeGPTCompletion(GroqGPTCompletion):
    PROMPT = """Give a challenge. You will be given previous 10 challenge.
    Your response should be only the challenge title.
    Note: no extra spaces and talks.
    example response: Foo bar baz
    """

    FALLBACK_RESULT = "Complete a 5K run in under 30 minutes"

    def clean_result(self, result):
        return result.strip()

    def is_valid_result(self, result):
        return re.match(r"^[a-zA-Z0-9 ]+$", result) is not None


class ChallengeStepsGPTCompletion(GroqGPTCompletion):
    PROMPT = """Break a challenge into several (maximum 5) steps.
    You will be given the challenge.
    Your response should be in the format of array of strings (JSON).
    I will parse your response as json so no extra spaces and talks.
    example: ["Foo", "Bar", "Baz"]
    """

    FALLBACK_RESULT = [
        "Identify the main objective",
        "Break down the objective into smaller steps",
        "Assign deadlines to each steps",
        "Gather necessary resources",
        "Review and adjust the plan",
    ]

    def clean_result(self, result):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return result

    def is_valid_result(self, result):
        return isinstance(result, list) and all(
            isinstance(step, str) for step in result
        )
