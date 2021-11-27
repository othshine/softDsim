from app.src.domain.scenario import TaskQueue
from app.src.domain.scenario import _TaskQueue

import pytest

from app.src.domain.team import Member


@pytest.fixture
def tq():
    return TaskQueue(easy=5, medium=10, hard=15)


def test_tq_initialize():
    tq = TaskQueue()
    assert tq.easy.todo == 0
    assert tq.medium.todo == 0
    assert tq.hard.todo == 0

    assert tq.easy.solved == 0
    assert tq.medium.solved == 0
    assert tq.hard.solved == 0


def test_tq_from_json():
    json = {'easy': {'todo': 5, 'solved': 5, 'error_unidentified': 2, 'error_identified': 15, 'tested': 900},
            'medium': {'todo': 10, 'solved': 0, 'error_unidentified': 4, 'error_identified': 23, 'tested': 435},
            'hard': {'todo': 15, 'solved': 0, 'error_unidentified': 23, 'error_identified': 1, 'tested': 0}
            }
    tq = TaskQueue(easy=json.get('easy'), medium=json.get('medium'), hard=json.get('hard'))
    assert tq.easy.todo == json.get('easy').get('todo')
    assert tq.easy.solved == json.get('easy').get('solved')
    assert tq.easy.error_unidentified == json.get('easy').get('error_unidentified')
    assert tq.easy.error_identified == json.get('easy').get('error_identified')
    assert tq.easy.tested == json.get('easy').get('tested')

    assert tq.medium.todo == json.get('medium').get('todo')
    assert tq.medium.solved == json.get('medium').get('solved')
    assert tq.medium.error_unidentified == json.get('medium').get('error_unidentified')
    assert tq.medium.error_identified == json.get('medium').get('error_identified')
    assert tq.medium.tested == json.get('medium').get('tested')

    assert tq.hard.todo == json.get('hard').get('todo')
    assert tq.hard.solved == json.get('hard').get('solved')
    assert tq.hard.error_unidentified == json.get('hard').get('error_unidentified')
    assert tq.hard.error_identified == json.get('hard').get('error_identified')
    assert tq.hard.tested == json.get('hard').get('tested')

def test_tq_to_json():
    tq = TaskQueue(easy=5, medium=10, hard=15)
    assert tq.json == {
        'easy': {
            'todo': 5,
            'solved': 0,
            'error_unidentified': 0,
            'error_identified': 0,
            'tested': 0
        },
        'medium': {
            'todo': 10,
            'solved': 0,
            'error_unidentified': 0,
            'error_identified': 0,
            'tested': 0
        },
        'hard': {
            'todo': 15,
            'solved': 0,
            'error_unidentified': 0,
            'error_identified': 0,
            'tested': 0
        }
    }


def test_task_queue_init(tq):
    assert tq.easy.todo == 5
    assert tq.medium.todo == 10
    assert tq.hard.todo == 15


def test_task_queue_len(tq):
    assert len(tq) == 30


def test_task_queue_solve_junior(tq):
    tq.solve(7, Member(skill_type='junior'))

    assert tq.easy.todo == 0
    assert tq.medium.todo == 8
    assert tq.hard.todo == 15

    assert tq.easy.done == 5
    assert tq.medium.done == 2
    assert tq.hard.done == 0


def test_task_queue_solve_senior(tq):
    tq.solve(2, Member(skill_type='senior'))

    assert tq.easy.todo == 5
    assert tq.medium.todo == 8
    assert tq.hard.todo == 15

    assert tq.easy.done == 0
    assert tq.medium.done == 2
    assert tq.hard.done == 0


def test_task_queue_solve_senior2(tq):
    tq.solve(25, Member(skill_type='senior'))

    assert tq.easy.todo == 0
    assert tq.medium.todo == 0
    assert tq.hard.todo == 5

    assert tq.easy.done == 5
    assert tq.medium.done == 10
    assert tq.hard.done == 10


def test_task_queue_solve_senior3(tq):
    tq.solve(14, Member(skill_type='senior'))

    assert tq.easy.todo == 3
    assert tq.medium.todo == 0
    assert tq.hard.todo == 13

    assert tq.easy.done == 2
    assert tq.medium.done == 10
    assert tq.hard.done == 2


def test_task_queue_solve_expert(tq):
    tq.solve(20, Member(skill_type='expert'))
    assert tq.easy.todo == 5
    assert tq.medium.todo == 5
    assert tq.hard.todo == 0

    assert tq.easy.done == 0
    assert tq.medium.done == 5
    assert tq.hard.done == 15


@pytest.fixture
def tq_inner():
    return _TaskQueue(todo=400, solved=25, error_unidentified=5)


def test_inner_tq_gets_initialized():
    tq = _TaskQueue()
    assert tq.todo == 0
    assert tq.solved == 0
    assert tq.error_unidentified == 0
    assert tq.error_identified == 0
    assert tq.tested == 0
    assert tq.done == 0

    tq = _TaskQueue(todo=400, solved=25, error_unidentified=5, error_identified=12, tested=50)
    assert tq.todo == 400
    assert tq.solved == 25
    assert tq.error_unidentified == 5
    assert tq.error_identified == 12
    assert tq.tested == 50
    assert tq.done == tq.solved + tq.error_unidentified


def test_inner_tq_json(tq_inner):
    assert tq_inner.json == {
        'todo': 400,
        'solved': 25,
        'error_unidentified': 5,
        'error_identified': 0,
        'tested': 0
    }
