import calendar
from django.core import management
from django.utils import timezone
from command_scheduler.enums import ScheduleType


class CommandSchedule:
    def __init__(self, type, *, day=1, weekday=calendar.FRIDAY, exclude=None):
        if exclude is None:
            exclude = []
        self.type = type
        self.day = day
        self.weekday = weekday
        self.exclude = exclude

    def should_run_today(self):
        now = timezone.now()
        if (
            self.type == ScheduleType.DAILY
            and now.weekday() not in self.exclude
        ):
            return True
        if self.type == ScheduleType.WEEKLY and self.weekday == now.weekday():
            return True
        if self.type == ScheduleType.MONTHLY and self.day == now.day():
            return True
        return False


class ScheduledCommand:
    def __init__(self, *, enabled=True, schedule, command, args=None):
        if args is None:
            args = {}
        self.enabled = enabled
        self.command = command
        self.schedule = schedule
        self.positional_args = args.get("args", [])
        self.optional_args = args.get("options", {})

    def run(self):
        management.call_command(
            self.command, *self.positional_args, **self.optional_args
        )


def args(*args, **kwargs):
    return {"args": args, "options": kwargs}
