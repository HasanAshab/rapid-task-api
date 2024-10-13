from ranker.users.models import User
from .gpt import DifficultyGPTCompletion
from .models import Difficulty


def suggest_difficulty_for(user: User, title: str) -> Difficulty:
    difficulties = list(Difficulty.objects.all().order_by("xp_value"))
    difficulty_map = {
        difficulty.pk: idx + 1 for idx, difficulty in enumerate(difficulties)
    }

    latest_completed_challenges = (
        user.challenge_set.completed()
        .order_by("-id")[:10]
        .values_list("title", "difficulty_id")
    )

    previous_challenges_str = "\n".join(
        [
            f"{challenge_title} --> {difficulty_map.get(difficulty_id)}"
            for challenge_title, difficulty_id in latest_completed_challenges
        ]
    )
    difficulty_count = len(difficulties)

    prompt = f"""
        Difficulty Score Range: 1 to {difficulty_count}
        User Info:
            Age: {user.age or "Not Available"}
            Gender: {user.gender}
            Level: {user.level}

        Previusly Completed Challenges with Difficulty:
            Title --> Score
            {previous_challenges_str or "Not Enough Data"}

        Title of the Challenge: {title}
    """
    completion = DifficultyGPTCompletion(prompt)
    difficulty_score = completion.create()

    return difficulties[difficulty_score - 1]
