from enum import Enum
from bson import ObjectId


class Task:
    def __init__(self, id=None, difficulty=None, done: bool = False, bug: bool = False, correct_specification: bool = True, done_by=None, pred=None) -> None:
        self.id = ObjectId() if id is None else id if isinstance(
            id, ObjectId) else ObjectId(id)
        self.difficulty = difficulty if isinstance(difficulty, Difficulty) else Difficulty(int(
            difficulty)) if isinstance(difficulty, int) or isinstance(difficulty, str) else Difficulty(1)
        self.done = done
        self.bug = bug
        self.correct_specification = correct_specification
        self.done_by = done_by if done_by is None or isinstance(
            done_by, ObjectId) else ObjectId(done_by)
        self.pred = pred if pred is None or isinstance(
            pred, ObjectId) else ObjectId(pred)

    @property
    def json(self):
        j = {
            'id': str(self.id),
            'difficulty': self.difficulty.value,
            'done': self.done,
            'bug': self.bug,
            'correct_specification': self.correct_specification
        }
        if self.done_by is not None:
            j['done_by'] = str(self.done_by)
        if self.pred is not None:
            j['pred'] = str(self.pred)

        return j

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
