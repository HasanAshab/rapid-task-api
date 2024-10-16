from django.conf import settings
from ranker.users.models import User
from .gpt import DifficultyGPTCompletion
from .models import Difficulty


def suggest_difficulty_for(user: User, title: str) -> Difficulty:
    latest_challenges = (
        user.challenge_set.not_ignored_for_ai()
        .select_related("difficulty")
        .order_by("-id")[: settings.DIFFICULTY_SUGGESTION_LOOKBACK_LIMIT]
    )

    previous_challenges_str = "\n".join(
        [
            f"{challenge.title} --> {challenge.get_difficulty_score()}"
            for challenge in latest_challenges
        ]
    )
    prompt = f"""
        User Info:
            Age: {user.age or "Not Available"}
            Gender: {user.gender}
            Level: {user.level}

        Previous Challenges with Difficulty Score:
            Title --> Score
            {previous_challenges_str or "Not Enough Data"}

        Title of the Challenge: {title}
    """
    completion = DifficultyGPTCompletion(prompt)
    difficulty_score = completion.create()

    return Difficulty.objects.filter(score__lte=difficulty_score).last()
