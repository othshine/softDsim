from dataclasses import dataclass


@dataclass
class Answer:
    def __init__(self, text: str, points: int, result_text: str = ""):
        self.text = text
        self.points = points
        self.result_text = result_text


class Decision:
    def __init__(self, text: str = "", continue_text: str = "Continue"):
        self.text = text
        self.answers = []
        self.continue_text = continue_text

    def __len__(self):
        return len(self.answers)

    def __dict__(self):
        return {'text': self.text,
                'answers': [dict(a) for a in self.answers],
                'continue_text': self.continue_text}

    def add(self, answer: Answer):
        self.answers.append(answer)

    def add_answer(self, text: str, points: int, *args):
        self.answers.append(Answer(text, points))

    def get_max_points(self):
        return max([a.points for a in self.answers])


@dataclass
class Scenario:
    def __init__(self, **kwargs):
        if json := kwargs.get('json'):
            self.build(json)
        else:
            self.tasks = kwargs.get('tasks', 0)
            self.actual_cost = kwargs.get('actual_cost', 0)
            self.budget = kwargs.get('budget', 0)
            self.current_day = kwargs.get('current_day', 0)
            self.scheduled_days = kwargs.get('scheduled_days', 0)
            self.counter = kwargs.get('counter', 0)
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
             'decisions': [dict(dec) for dec in self._decisions],
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
                      decisions=json.get('decisions'),
                      _id=json.get('_id')
                      )
