from dataclasses import dataclass


@dataclass(frozen=True)
class WorkPackage:
    days: int
    daily_meeting_hours: int

    @property
    def total_work_hours(self):
        return (8 - self.daily_meeting_hours) * self.days

    @property
    def total_meeting_hours(self):
        return self.daily_meeting_hours*self.days


@dataclass(frozen=False)
class WorkResult:
    tasks_completed: int = 0
    unidentified_errors: int = 0
    fixed_errors: int = 0
