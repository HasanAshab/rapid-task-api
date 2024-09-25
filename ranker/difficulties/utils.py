from ranker.users.models import User
from .gpt import DifficultyGPTCompletion
from .models import Difficulty


def suggest_difficulty_for(user: User, title: str) -> Difficulty:
    latest_completed_challenges = (
        user.challenge_set.completed()
        .select_related("difficulty")
        .order_by("-id")[:10]
        .values_list("title", "difficulty__slug")
    )
    previous_challenges_str = "\n".join(
        [
            f"{challenge_title} --> {difficulty_slug}"
            for challenge_title, difficulty_slug in latest_completed_challenges
        ]
    )
    difficulty_slugs = Difficulty.objects.values_list("slug", flat=True)
    completion = DifficultyGPTCompletion(
        f"""
            Available Difficulties: {", ".join(difficulty_slugs)}
            User Info:
                Age: {user.age or "Not Available"}
                Gender: {user.gender}
                Level: {user.level}
            Previusly Completed Challenges with Difficulty:
                {previous_challenges_str or "Not Enough Data"}
            Title of the Challenge: {title}
        """
    )
    difficulty_slug = completion.create()
    return Difficulty.objects.get(slug=difficulty_slug)
