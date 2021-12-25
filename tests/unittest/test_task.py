import pytest

from bson import ObjectId

from app.src.domain.task import Task, Difficulty
from app.src.domain.team import Member


def test_instantiate_task():
    t = Task()


def test_task_has_id():
    t = Task()
    assert isinstance(t.id, ObjectId)


def test_task_difficulty():
    t1 = Task(difficulty=2)
    assert t1.difficulty == Difficulty.MEDIUM

    t2 = Task(difficulty=Difficulty.HARD)
    assert t2.difficulty == Difficulty.HARD

    t3 = Task()
    assert t3.difficulty == Difficulty.EASY

    t4 = Task(difficulty="2")
    assert t4.difficulty == Difficulty.MEDIUM


def test_task_bool_attributes():
    t = Task()

    assert t.done == False
    assert t.bug == False
    assert t.correct_specification == True

    t2 = Task(done=True, bug=True, correct_specification=False)

    assert t2.done == True
    assert t2.bug == True
    assert t2.correct_specification == False


def test_done_by():
    m = Member()
    t = Task(done_by=m.id)

    m2 = Member()
    t2 = Task(done_by=str(m2.id))

    assert isinstance(t.done_by, ObjectId)
    assert isinstance(t2.done_by, ObjectId)

    assert t.done_by == m.id
    assert t2.done_by == m2.id
    assert t.done_by != m2.id
    assert t.done_by != t2.done_by


def test_predecessor():
    t0 = Task()
    t1 = Task(pred=t0.id)

    assert t0.pred is None
    assert t1.pred == t0.id


def test_task_to_json():
    _id = ObjectId()
    m = Member()
    t = Task(id=_id, difficulty=3, done=True, bug=False, done_by=m.id)

    json = {
        'id': str(_id),
        'difficulty': 3,
        'done': True,
        'bug': False,
        'correct_specification': True,
        'done_by': str(m.id)
    }

    assert t.json == json
    assert t.json.get('pred') is None

    _id2 = ObjectId()
    t2 = Task(id=_id2, difficulty=Difficulty.MEDIUM,
              pred=t.id, correct_specification=False)

    json2 = {
        'id': str(_id2),
        'difficulty': 2,
        'done': False,
        'bug': False,
        'correct_specification': False,
        'pred': str(t.id),
    }

    assert t2.json == json2
    assert t2.json.get('done_by') is None
