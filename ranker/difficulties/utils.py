from ranker.users.models import User
from .gpt import DifficultyGPTCompletion
from .models import Difficulty


def suggest_difficulty_for(user: User, title: str) -> Difficulty:
    latest_challenges = (
        user.challenge_set.select_related("difficulty")
        .order_by("-id")[:10]
        .values_list("title", "difficulty__slug")
    )
    previous_challenges_str = "\n".join(
        [
            f"{challenge_title} --> {difficulty_slug}"
            for challenge_title, difficulty_slug in latest_challenges
        ]
    )
    difficulty_slugs = Difficulty.objects.values_list("slug", flat=True)
    completion = DifficultyGPTCompletion(
        f"""
            Available Difficulties: {", ".join(difficulty_slugs)}
            User Info:
                Age: {user.age or "No Enough Data"}
                Gender: {user.gender}
                Level: {user.level}
            Previus Challenges with Difficulty:
                {previous_challenges_str or "No Enough Data"}
            Title of the Challenge: {title}
        """
    )
    difficulty_slug = completion.create()
    return Difficulty.objects.get(slug=difficulty_slug)
