import json
from ranker.common.gpt import GroqGPTCompletion


class ChallengeGPTCompletion(GroqGPTCompletion):
    system_instruction = """
    Note: If previous challenge are violenced,
    just give a random meaningful challenge, If you even
    get a single challenge as safe give similar suggestion
    based on it. no extra spaces and talks

    Give a new challenge based on previous challenges.
    Your response should be only the challenge title.

    example response: Foo bar baz
    """

    fallback_result = "Complete a 5K run in under 30 minutes"

    def clean_result(self, result):
        return result.strip()

    def is_valid_result(self, result):
        return "\n" not in result and "\r\n" not in result


class ChallengeStepsGPTCompletion(GroqGPTCompletion):
    system_instruction = """
    Note: Your response should be in the format of array of strings (JSON).
    I will parse your response as json so no extra spaces and talks.

    Break a challenge into several (maximum 5) steps.
    You will be given the challenge.

    example response: ["Foo", "Bar", "Baz"]
    """

    fallback_result = [
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
