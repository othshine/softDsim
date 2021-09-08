from dataclasses import dataclass
from typing import List

from bson import ObjectId

from app.src.domain.team import Team, Member


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


class Decision:
    def __init__(self, text: List[TextBlock] = None, continue_text: str = "Continue", dtype: str = None,
                 points: int = 0):
        self.text = text
        self.answers = []
        self.continue_text = continue_text
        self.dtype = dtype
        self.points = points

    def __len__(self):
        return len(self.answers)

    @property
    def json(self):
        return {'text': [t.json for t in self.text],
                'answers': [a.json for a in self.answers],
                'continue_text': self.continue_text,
                'dtype': self.dtype,
                'points': self.points}

    def add(self, answer: Answer):
        self.answers.append(answer)

    def add_answer(self, text: str, points: int, *args):
        self.answers.append(Answer(text, points))

    def get_max_points(self):
        return max([a.points for a in self.answers])

    def add_text_block(self, header: str, content: str):
        t = TextBlock(header, content)
        if self.text:
            self.text.append(t)
        else:
            self.text = [t]

    def evaluate(self, answer_text):
        self.points = self.get_points_for(answer_text)

    def get_points_for(self, answer_text: str) -> int:
        for a in self.answers:
            if answer_text == a.text:
                return a.points
        return 0


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
            self.counter = int(kwargs.get('counter', 0) or 0)
            self._decisions = kwargs.get('decisions', []) or []
            self.id = ObjectId(kwargs.get('id')) or ObjectId
            self.desc = kwargs.get('desc', 0) or ""
            self.team = Team()

    def __iter__(self):
        return self

    def __next__(self) -> Decision:
        if self.counter >= len(self._decisions):
            raise StopIteration
        self.counter += 1
        return self._decisions[self.counter - 1]

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
             '_id': str(self.id)
             }
        return d

    def add(self, decision: Decision):
        self._decisions.append(decision)

    def remove(self, index: int):
        del self._decisions[index]

    def get_max_points(self) -> int:
        return sum([d.get_max_points() for d in self._decisions])

    def build(self, json):  # ToDo: Refactor.
        self.__init__(tasks_done=json.get('tasks_done'),
                      tasks_total=json.get('tasks_total'),
                      scheduled_days=json.get('scheduled_days'),
                      actual_cost=json.get('actual_cost'),
                      current_day=json.get('current_day'),
                      budget=json.get('budget'),
                      id=json.get('_id'),
                      desc=json.get('desc'),
                      )
        for d in json.get('decisions') or []:
            dec = Decision(continue_text=d.get('continue_text'), dtype=d.get('dtype'), points=d.get('points'))
            for t in d.get('text'):
                dec.add_text_block(t.get('header'), t.get('content'))
            for a in d.get('answers'):
                dec.add(Answer(text=a.get('text'), points=a.get('points'), result_text=a.get('result_text')))
            self.add(dec)
        if t := json.get('team'):
            for m in t.get('staff'):
                member = Member(m.get('skill-type'), xp_factor=m.get('xp'), motivation=m.get('motivation'),
                                familiarity=m.get('familiarity'), id=m.get('_id'))
                if m.get('halted'):
                    member.halt()
                self.team += member

    def get_id(self) -> str:
        return str(self.id)
