
class Scenario:
    def __init__(self, tasks: int, budget: int, scheduled_days: int):
        self.tasks = tasks
        self.actual_cost = 0
        self.budget = budget
        self.current_day = 0
        self.scheduled_days = scheduled_days
