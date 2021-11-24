from dataclasses import dataclass


@dataclass(frozen=True)
class WorkPackage:
    days: int
    meeting_hours: int
    training_hours: int
    tasks_easy: int
    tasks_medium: int
    tasks_hard: int
    unidentified_errors: int
    identified_errors: int
    quality_check: bool
    error_fixing: bool
    total_tasks_done: int

    @property
    def daily_work_hours(self):
        return 8 - self.meeting_hours  # ToDo: support for overtime.


@dataclass(frozen=False)
class WorkResult:
    tasks_easy_completed: int = 0
    tasks_medium_completed: int = 0
    tasks_hard_completed: int = 0
    unidentified_errors: int = 0
    identified_errors: int = 0
    fixed_errors: int = 0

    def __add__(self, other):
        self.tasks_easy_completed += other.tasks_easy_completed
        self.tasks_medium_completed += other.tasks_medium_completed
        self.tasks_hard_completed += other.tasks_hard_completed
        self.unidentified_errors += other.unidentified_errors
        self.identified_errors += other.identified_errors
        self.fixed_errors += other.fixed_errors
        return self


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
