from dataclasses import dataclass


@dataclass(frozen=True)
class WorkPackage:
    days: int
    daily_meeting_hours: int
    tasks: int
    unidentified_errors: int
    identified_errors: int
    quality_check: bool
    error_fixing: bool

    @property
    def daily_work_hours(self):
        return 8 - self.daily_meeting_hours  # ToDo: support for overtime.


@dataclass(frozen=False)
class WorkResult:
    tasks_completed: int = 0
    unidentified_errors: int = 0
    identified_errors: int = 0
    fixed_errors: int = 0


@dataclass(frozen=True)
class SimulationGoal:
    tasks: int = None

    @property
    def json(self):
        return {'tasks': self.tasks}

    def reached(self, tasks: int = 0):
        if self.tasks and self.tasks > tasks:
            return False
        return True
