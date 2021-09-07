from dataclasses import dataclass


@dataclass(frozen=True)
class WorkPackage:
    days: int
    daily_meeting_hours: int

    @property
    def work_hours(self):
        return 8 - (self.daily_meeting_hours)


@dataclass(frozen=False)
class WorkResult:
    tasks_completed: int = 0
    unidentified_errors: int = 0
    fixed_errors: int = 0
