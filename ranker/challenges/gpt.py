from ranker.common import gpt
from typing_extensions import TypedDict


class ChallengeGroup(TypedDict):
    group: str
    challenges: list[int]


class GroupChallengeGPTCompletion(gpt.GeminiJSONGPTCompletion):
    response_schema = list[ChallengeGroup]

    system_instruction = """
    You are a challenge grouper.

    You will be provided a list of challenges with their index.
    group the challenges based on their similarities. if some
    challenges are not similar, add them to `others` group.

    for example:
    push ups, planks, squats will be in the same group `Workouts`
    extract data from people will be in the same group `Manupilation`
    foo, bar, baz will be in the same group `Others`
    """


class ChallengeGPTCompletion(gpt.GeminiGPTCompletion):
    system_instruction = """
    You are a challenge generator.

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


class ChallengeStepsGPTCompletion(gpt.GeminiJSONGPTCompletion):
    response_schema = list[str]

    system_instruction = """
    You are a challenge steps generator.
    Break a challenge into several (maximum 5) steps.
    You will be given the challenge.
    """

    fallback_result = [
        "Identify the main objective",
        "Break down the objective into smaller steps",
        "Assign deadlines to each steps",
        "Gather necessary resources",
        "Review and adjust the plan",
    ]
