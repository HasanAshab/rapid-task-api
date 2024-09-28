from django.db import transaction
from ranker.users.models import User
from .gpt import ChallengeGPTCompletion, ChallengeStepsGPTCompletion
from .models import Challenge, ChallengeStep


def suggest_challenge_title(user: User) -> Challenge:
    latest_challenges = user.challenge_set.order_by("-id")[:10].values_list(
        "title", flat=True
    )
    joined_titles = ", ".join(latest_challenges)
    print(joined_titles)
    completion = ChallengeGPTCompletion(joined_titles)
    return completion.create()


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
