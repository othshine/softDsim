from dataclasses import dataclass, field
from typing import Optional, List

from bson import ObjectId

from app.src.domain.dataObjects import WorkPackage, WorkResult, SimulationGoal
from app.src.domain.decision_tree import ActionList, Decision, SimulationDecision, AnsweredDecision
from app.src.domain.team import Team, Member
from utils import month_to_day


@dataclass
class Scenario:
    name: str
    tasks_total: int
    budget: int
    scheduled_days: int
    decisions: list = field(default_factory=list)
    id: ObjectId = ObjectId()
    desc: str = ""

    def add(self, decision):
        self.decisions.append(decision)

    @property
    def json(self):
        return {'name': self.name,
                'decisions': [dec.json for dec in self.decisions],
                'tasks_total': self.tasks_total,
                'budget': self.budget,
                'scheduled_days': self.scheduled_days,
                '_id': str(self.id),
                'id': str(self.id),
                'desc': self.desc
                }


class UserScenario:
    def __init__(self, **kwargs):
        self.tasks_done = int(kwargs.get('tasks_done', 0) or 0)
        self.actual_cost = int(kwargs.get('actual_cost', 0) or 0)
        self.current_day = int(kwargs.get('current_day', 0) or 0)
        self.counter = int(kwargs.get('counter', -1))
        self.decisions = kwargs.get('decisions', []) or []
        self.id = ObjectId(kwargs.get('id')) or ObjectId()
        self.actions = kwargs.get('actions') or ActionList()
        self.team = Team()
        self.user = kwargs.get('user')
        self.template: Scenario = kwargs.get('scenario')

    def __iter__(self):
        return self

    def __next__(self) -> Decision:
        self._eval_counter()
        if self.counter >= len(self.decisions):
            raise StopIteration
        return self.decisions[self.counter]

    def __len__(self) -> int:
        return len(self.decisions)

    def __eq__(self, other):
        if isinstance(other, Scenario):
            return self.id == other.id
        return False

    @property
    def json(self):
        d = {'tasks_done': self.tasks_done,
             'decisions': [dec.json for dec in self.decisions],
             'actual_cost': self.actual_cost,
             'counter': self.counter,
             'current_day': self.current_day,
             'team': self.team.json,
             '_id': str(self.id),
             'id': str(self.id),
             'user': self.user,
             'actions': self.actions.json,
             'template_id': str(self.template.id)
             }
        return d

    def add(self, decision: Decision):
        self.decisions.append(decision)

    def remove(self, index: int):
        del self.decisions[index]

    @property
    def button_rows(self):
        json = []
        d = self.decisions[self.counter]
        if isinstance(d, SimulationDecision):
            for a in d.active_actions or []:
                if (action := self.actions.get(a)) is not None:
                    json.append(action.json)
        else:
            for action in d.actions or []:
                json.append(action.json)
        return json

    @property
    def numeric_rows(self):
        json = []
        d = self.decisions[self.counter]
        for aa in d.active_actions:
            if aa == 'staff-pick':  # ToDo: Make this quick and dirty solution dynamic.
                json.append({
                    'title': "staff",
                    'values':
                        {
                            'junior': self.team.count('junior'),
                            'senior': self.team.count('senior'),
                            'expert': self.team.count('expert')
                        }
                })
        return json

    def get_max_points(self) -> int:
        return sum([d.get_max_points() for d in self.decisions])

    def work(self, days, meeting):
        wp = WorkPackage(days=days, daily_meeting_hours=meeting)
        wr = self.team.work(wp)
        self._apply_work_result(wr)
        self.actual_cost += month_to_day(self.team.salary, days)
        self.current_day += days

    def _apply_work_result(self, wr: WorkResult):
        self.tasks_done += wr.tasks_completed

    def get_id(self) -> str:
        return str(self.id)

    def _eval_counter(self):
        """
        Increases the value of the counter by one of the current decision is done.
        """
        if self.counter == -1:
            self.counter = 0
        else:
            d = self.decisions[self.counter]
            if (not isinstance(d, SimulationDecision)) or (
                    isinstance(d, SimulationDecision) and d.goal.reached(tasks=self.tasks_done)):
                self.counter += 1

    def get_decision(self, nr: int = None) -> Optional[Decision]:
        if nr is None:
            nr = self.counter
        if nr < 0:
            return None
        return self.decisions[nr]

    def total_score(self) -> int:
        p = 0
        for d in self.decisions:
            p += d.points
        return p
