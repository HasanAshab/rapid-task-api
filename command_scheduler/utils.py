import calendar
from django.core import management
from django.utils import timezone
from command_scheduler.enums import ScheduleType


class CommandSchedule:
    def __init__(self, schedule):
        self._schedule = schedule
        self.day = 1
        self.weekday = calendar.FRIDAY
        self.exclude = []
        if isinstance(schedule, dict):
            self.type = schedule["type"]
            if "day" in schedule:
                self.day = schedule["day"]
            if "weekday" in schedule:
                self.weekday = schedule["weekday"]
            if "exclude" in schedule:
                self.exclude = schedule["exclude"]
        else:
            self.type = schedule

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
    def __init__(self, config):
        args = config.get("args", {})
        self._config = config
        self.name = config["command"]
        self.schedule = CommandSchedule(config["schedule"])
        self.positional_args = args.get("args", [])
        self.optional_args = args.get("options", {})

    def is_enabled(self):
        return self._config.get("enabled", True)

    def run(self):
        management.call_command(
            self.name, *self.positional_args, **self.optional_args
        )


def args(*args, **kwargs):
    return {"args": args, "options": kwargs}
