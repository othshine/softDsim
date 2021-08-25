from dataclasses import dataclass


@dataclass
class Answer:
    def __init__(self, text: str, points: int, result_text: str = ""):
        self.text = text
        self.points = points
        self.result_text = result_text


class Decision:
    def __init__(self, text: str = ""):
        self.text = text
        self.answers = []

    def __len__(self):
        return len(self.answers)

    def add(self, answer: Answer):
        self.answers.append(answer)

    def add_answer(self, text: str, points: int, *args):
        self.answers.append(Answer(text, points))

    def get_max_points(self):
        return max([a.points for a in self.answers])


class Scenario:
    def __init__(self):
        self.counter = 0
        self._decisions = []

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter >= len(self._decisions):
            raise StopIteration
        self.counter += 1
        return self._decisions[self.counter-1]

    def __len__(self):
        return len(self._decisions)

    def add(self, decision: Decision):
        self._decisions.append(decision)

    def remove(self, index: int):
        del self._decisions[index]

    def get_max_points(self):
        return sum([d.get_max_points() for d in self._decisions])
