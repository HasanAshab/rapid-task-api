from django.db import transaction
from ranker.difficulties.utils import suggest_difficulty_for
from ranker.users.models import User
from .gpt import ChallengeGPTCompletion, ChallengeStepsGPTCompletion
from .models import Challenge, ChallengeStep


def suggest_challenge_title(user: User) -> str:
    latest_challenges = (
        user.challenge_set.not_ignored_for_ai()
        .order_by("-id")[:10]
        .values_list("title", flat=True)
    )
    joined_titles = ", ".join(latest_challenges)
    completion = ChallengeGPTCompletion(joined_titles)
    return completion.create()


def suggest_challenge(user: User) -> Challenge:
    challenge_title = suggest_challenge_title(user)
    difficulty = suggest_difficulty_for(user, challenge_title)
    challenge = Challenge(
        user=user,
        difficulty=difficulty,
        title=challenge_title,
    )
    return challenge


def generate_challenge_steps(challenge: Challenge) -> list[ChallengeStep]:
    completion = ChallengeStepsGPTCompletion(challenge.title)
    challenge_steps_titles = completion.create()
    challenge_steps = [
        ChallengeStep(challenge=challenge, title=title)
        for title in challenge_steps_titles
    ]
    with transaction.atomic():
        challenge.steps.all().delete()
        challenge_steps = ChallengeStep.objects.bulk_create(challenge_steps)
    return challenge_steps
