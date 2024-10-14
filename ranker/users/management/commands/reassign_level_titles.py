from django.core.management.base import BaseCommand
from ranker.users.models import User
from ranker.level_titles.models import LevelTitle
from ranker.common.utils import chunk_queryset


class Command(BaseCommand):
    help = (
        "Reassign relevant level titles to all users based on their current XP"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--chunk",
            type=int,
            default=1000,
            help="Chunk size",
        )

    def handle(self, **options):
        level_titles = list(
            LevelTitle.objects.all().order_by("-required_level")
        )

        for user_chunk in chunk_queryset(User.objects.all(), options["chunk"]):
            users_to_update = []
            for user in user_chunk:
                level_title = next(
                    (
                        level_title
                        for level_title in level_titles
                        if level_title.required_level <= user.level
                        and user.level_title != level_title
                    ),
                    None,
                )
                if level_title:
                    user.level_title = level_title
                    users_to_update.append(user)
            User.objects.bulk_update(users_to_update, ["level_title"])

        self.stdout.write(
            self.style.SUCCESS("Successfully reassigned level titles.")
        )
