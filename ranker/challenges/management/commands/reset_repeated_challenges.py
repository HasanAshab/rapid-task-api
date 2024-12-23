from django.core.management.base import (
    BaseCommand,
)
from django.db import transaction
from ranker.common.utils import chunk_queryset
from ranker.users.models import User
from ranker.challenges.models import Challenge


class Command(BaseCommand):
    help = "Reset repeated challenges of all users"

    def add_arguments(self, parser):
        parser.add_argument(
            "repeat_type",
            type=str,
            choices=[
                Challenge.RepeatType.DAILY,
                Challenge.RepeatType.WEEKLY,
                Challenge.RepeatType.MONTHLY,
            ],
            help="Repeat type to reset",
        )
        parser.add_argument(
            "--chunk",
            type=int,
            default=1000,
            help="Chunk size",
        )
        parser.add_argument(
            "--no-xp",
            action="store_true",
            help="If specified, XP will not be mutated",
        )

    def handle(self, repeat_type, **options):
        if options["no_xp"]:
            Challenge.objects.repeated(repeat_type).mark_as_active()
            return self.stdout.write(
                self.style.SUCCESS(
                    "Successfully reset daily challenges without mutating xp"
                )
            )

        daily_challenges = (
            Challenge.objects.active()
            .repeated(repeat_type)
            .select_related("user")
        )
        for challenge_chunk in chunk_queryset(
            daily_challenges, options["chunk"]
        ):
            user_updates = {}
            for challenge in challenge_chunk:
                if challenge.user.pk in user_updates:
                    challenge.user = user_updates[challenge.user.pk]
                if challenge.snooze_for_today:
                    challenge.snooze_for_today = False
                else:
                    challenge.penalize_failure_xp(commit=False)
                challenge.mark_as_active(commit=False)
                user_updates[challenge.user.pk] = challenge.user

            with transaction.atomic():
                Challenge.objects.bulk_update(
                    challenge_chunk, ["status", "snooze_for_today"]
                )
                User.objects.bulk_update(user_updates.values(), ["total_xp"])
        Challenge.objects.repeated(repeat_type).inactive().mark_as_active()

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully reset daily challenges of all users"
            )
        )
