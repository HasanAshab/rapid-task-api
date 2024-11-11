from django.conf import settings
from django.core.management.base import (
    BaseCommand,
)


class Command(BaseCommand):
    help = "Run scheduled commands"

    def handle(self, *args, **kwargs):
        for scheduled_command in settings.SCHEDULED_COMMANDS:
            if not scheduled_command.enabled:
                continue
            if scheduled_command.schedule.should_run_today():
                scheduled_command.run()
