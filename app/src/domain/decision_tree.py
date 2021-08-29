from dataclasses import dataclass
from typing import List


@dataclass
class Answer:
    def __init__(self, text: str, points: int, result_text: str = ""):
        self.text = text
        self.points = points
        self.result_text = result_text

    @property
    def json(self):
        return {'text': self.text,
                'points': self.points,
                'result_text': self.result_text}


@dataclass
class TextBlock(object):
    def __init__(self, header: str, content: str):
        self.header = header
        self.content = content

    @property
    def json(self):
        return {'header': self.header,
                'content': self.content}


@dataclass
class Decision:
    def __init__(self, text: List[TextBlock] = None, continue_text: str = "Continue"):
        self.text = text
        self.answers = []
        self.continue_text = continue_text

    def __len__(self):
        return len(self.answers)

    @property
    def json(self):
        return {'text': [t.json for t in self.text],
                'answers': [a.json for a in self.answers],
                'continue_text': self.continue_text}

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


@dataclass
class Scenario:
    def __init__(self, **kwargs):
        if json := kwargs.get('json'):
            self.build(json)
        else:
            self.tasks = int(kwargs.get('tasks', 0))
            self.actual_cost = int(kwargs.get('actual_cost', 0))
            self.budget = int(kwargs.get('budget', 0))
            self.current_day = int(kwargs.get('current_day', 0))
            self.scheduled_days = int(kwargs.get('scheduled_days', 0))
            self.counter = int(kwargs.get('counter', 0))
            self._decisions = kwargs.get('decisions', [])
            self.id_ = kwargs.get('_id', None)

    def __iter__(self):
        return self

    def __next__(self) -> Decision:
        if self.counter >= len(self._decisions):
            raise StopIteration
        self.counter += 1
        return self._decisions[self.counter - 1]

    def __len__(self) -> int:
        return len(self._decisions)

    @property
    def json(self):
        d = {'tasks': self.tasks,
             'decisions': [dec.json for dec in self._decisions],
             'actual_cost': self.actual_cost,
             'budget': self.budget,
             'counter': self.counter,
             'current_day': self.current_day,
             'scheduled_days': self.scheduled_days,
             }
        if self.id_:
            d['id'] = self.id_
        return d

    def add(self, decision: Decision):
        self._decisions.append(decision)

    def remove(self, index: int):
        del self._decisions[index]

    def get_max_points(self) -> int:
        return sum([d.get_max_points() for d in self._decisions])

    def build(self, json):
        self.__init__(tasks=json.get('tasks'),
                      scheduled_days=json.get('scheduled_days'),
                      actual_cost=json.get('actual_cost'),
                      current_day=json.get('current_day'),
                      budget=json.get('budget'),
                      _id=json.get('_id')
                      )
        for d in json.get('decisions'):
            dec = Decision(continue_text=d.get('continue_text'))
            for t in d.get('text'):
                dec.add_text_block(t.get('header'), t.get('content'))
            for a in d.get('answers'):
                dec.add(Answer(text=a.get('text'), points=a.get('points'), result_text=a.get('result_text')))
            self.add(dec)

    def get_id(self):
        return self.id_

