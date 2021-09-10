from abc import ABC
from dataclasses import dataclass
from typing import List

from bson import ObjectId

from app.src.domain.dataObjects import WorkPackage, WorkResult, SimulationGoal
from app.src.domain.team import Team, Member
from utils import month_to_day


@dataclass
class Answer:
    text: str
    points: int
    result_text: str = None

    @property
    def json(self):
        return {'text': self.text,
                'points': self.points,
                'result_text': self.result_text}


@dataclass
class TextBlock(object):
    header: str
    content: str

    @property
    def json(self):
        return {'header': self.header,
                'content': self.content}


class Decision(ABC):
    def __init__(self, **kwargs):
        self.text: List[TextBlock] = kwargs.get('text', None)
        self.continue_text: str = kwargs.get('continue_text', "Continue")
        self.points = kwargs.get('points', 0)

    @property
    def json(self):
        data = {'continue_text': self.continue_text,
                'points': self.points}
        if self.text:
            data = {**data, 'text': [t.json for t in self.text]}
        return data

    def get_max_points(self):
        pass

    def add_text_block(self, header: str, content: str):
        t = TextBlock(header, content)
        if self.text:
            self.text.append(t)
        else:
            self.text = [t]

    def evaluate(self, answer_text):
        # self.points = self.get_points_for(answer_text)
        pass


class AnsweredDecision(Decision):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answers = kwargs.get('answers', [])

    def __len__(self):
        return len(self.answers)

    @property
    def json(self):
        return {**super().json, 'answers': [a.json for a in self.answers]}

    def add(self, answer: Answer):
        self.answers.append(answer)

    def add_answer(self, text: str, points: int, *args):
        self.answers.append(Answer(text, points))

    def get_max_points(self):
        return max([a.points for a in self.answers])

    def get_points_for(self, answer_text: str) -> int:
        for a in self.answers:
            if answer_text == a.text:
                return a.points
        return 0


class SimulationDecision(Decision):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.goal: SimulationGoal = kwargs.get('goal')
        self.max_points: int = kwargs.get('max_points', 0)

    def set_goal(self, goal: SimulationGoal):
        self.goal = goal

    def get_max_points(self) -> int:
        return self.max_points


class Scenario:
    def __init__(self, **kwargs):
        if json := kwargs.get('json'):
            self.build(json)
        else:
            self.tasks_done = int(kwargs.get('tasks_done', 0) or 0)
            self.tasks_total = int(kwargs.get('tasks_total', 0) or 0)
            self.actual_cost = int(kwargs.get('actual_cost', 0) or 0)
            self.budget = int(kwargs.get('budget', 0) or 0)
            self.current_day = int(kwargs.get('current_day', 0) or 0)
            self.scheduled_days = int()
            self.counter = int(kwargs.get('counter', -1) or -1)
            self._decisions = kwargs.get('decisions', []) or []
            self.id = ObjectId(kwargs.get('id')) or ObjectId()
            self.desc = kwargs.get('desc', 0) or ""
            self.team = Team()
            self.name = kwargs.get("name", "DefaultName")

    def __iter__(self):
        return self

    def __next__(self) -> Decision:
        if self.counter >= len(self._decisions) - 1:
            raise StopIteration
        self._eval_counter()
        return self._decisions[self.counter]

    def __len__(self) -> int:
        return len(self._decisions)

    def __eq__(self, other):
        if isinstance(other, Scenario):
            return self.id == other.id
        return False

    @property
    def json(self):
        d = {'tasks_done': self.tasks_done,
             'tasks_total': self.tasks_total,
             'decisions': [dec.json for dec in self._decisions],
             'actual_cost': self.actual_cost,
             'budget': self.budget,
             'counter': self.counter,
             'current_day': self.current_day,
             'scheduled_days': self.scheduled_days,
             'desc': self.desc,
             'team': self.team.json,
             '_id': str(self.id),
             'name': self.name
             }
        return d

    def add(self, decision: Decision):
        self._decisions.append(decision)

    def remove(self, index: int):
        del self._decisions[index]

    def get_max_points(self) -> int:
        return sum([d.get_max_points() for d in self._decisions])

    def work(self, days, meeting):
        wp = WorkPackage(days=days, daily_meeting_hours=meeting)
        self._apply_work_result(self.team.work(wp))
        self.actual_cost += month_to_day(self.team.salary, days)
        self.current_day += days

    def _apply_work_result(self, wr: WorkResult):
        self.tasks_done += wr.tasks_completed

    def build(self, json):  # ToDo: Refactor.
        self.__init__(tasks_done=json.get('tasks_done'),
                      tasks_total=json.get('tasks_total'),
                      scheduled_days=json.get('scheduled_days'),
                      actual_cost=json.get('actual_cost'),
                      current_day=json.get('current_day'),
                      budget=json.get('budget'),
                      id=json.get('_id'),
                      desc=json.get('desc'),
                      name=json.get('name')
                      )
        for d in json.get('decisions') or []:
            self.add(build_decision(d))
        if t := json.get('team'):
            for m in t.get('staff'):
                member = Member(m.get('skill-type'), xp_factor=m.get('xp'), motivation=m.get('motivation'),
                                familiarity=m.get('familiarity'), id=m.get('_id'))
                if m.get('halted'):
                    member.halt()
                self.team += member

    def get_id(self) -> str:
        return str(self.id)

    def _eval_counter(self):
        """
        Increases the value of the counter by one of the current decision is done.
        """
        if self.counter == -1:
            self.counter = 0
        else:
            d = self._decisions[self.counter]
            if not isinstance(d, SimulationDecision) or (
                    isinstance(d, SimulationDecision) and d.goal.reached(tasks=self.tasks_done)):
                self.counter += 1


def build_decision(d):
    if d.get('goal'):
        dec = SimulationDecision(goal=SimulationGoal(**d.get('goal')))
    else:
        dec = AnsweredDecision()
        for a in d.get('answers') or []:
            dec.add(Answer(text=a.get('text'), points=a.get('points'), result_text=a.get('result_text')))

    for t in d.get('text') or []:
        dec.add_text_block(t.get('header'), t.get('content'))
    dec.points = d.get('points', 0)

    return dec
