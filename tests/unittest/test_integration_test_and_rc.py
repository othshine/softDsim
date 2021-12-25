import pytest

from app.src.domain.integration_test import integration_test
from app.src.domain.scenario import TaskQueue, _TaskQueue

@pytest.fixture
def tq():
    e = _TaskQueue(todo=20, solved=100, error_unidentified=10, error_identified=30, unit_tested=300)
    m = _TaskQueue(todo=0, solved=0, error_unidentified=0, error_identified=0, unit_tested=100)
    h = _TaskQueue(todo=0, solved=50, error_unidentified=0, error_identified=0, unit_tested=200)
    return TaskQueue(easy=e, medium=m, hard=h)

def test_inteagration_test(tq: TaskQueue):
    assert tq.total_integration_tested == 0
    integration_test(tq=tq)
    assert tq.total_integration_tested > 0