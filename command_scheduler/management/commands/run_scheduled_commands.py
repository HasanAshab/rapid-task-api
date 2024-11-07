from django.conf import settings
from django.core.management.base import (
    BaseCommand,
)
from command_scheduler.utils import ScheduledCommand


class Command(BaseCommand):
    help = "Run scheduled commands"

    def handle(self, *args, **kwargs):
        for config in settings.SCHEDULED_COMMANDS:
            scheduled_command = ScheduledCommand(config)
            if not scheduled_command.is_enabled():
                continue
            if scheduled_command.schedule.should_run_today():
                scheduled_command.run()
