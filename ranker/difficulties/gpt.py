from ranker.common.gpt import GeminiGPTCompletion


class DifficultyGPTCompletion(GeminiGPTCompletion):
    system_instruction = """
    You are a difficulty detector.

    Note: response should be only the difficulty score.
    no extra spaces and talks.

    Suggest difficulty for the challenge.
    You will be provided score range of difficulty (float not allowed),
    info of the user, previously completed challenges with their
    difficulty score and the challenge thats difficulty to be detected.

    example response: 5
    """

    fallback_result = 2

    def clean_result(self, result):
        return int(result.strip())

    def is_valid_result(self, result):
        return isinstance(result, int)
