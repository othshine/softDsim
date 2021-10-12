from utils import get_active_label, weighted


def test_get_active_label():
    a = get_active_label([{'label': 'Agile', 'active': False}, {'label': 'Incremental', 'active': False},
                          {'label': 'Iterative', 'active': False}, {'label': 'Predictive', 'active': True}])
    assert a == "Predictive"

    a = get_active_label([{'label': 'Agile', 'active': True}, {'label': 'Incremental', 'active': False},
                          {'label': 'Iterative', 'active': False}])
    assert a == "Agile"

    a = get_active_label([])
    assert a is None

    a = get_active_label(
        [{'label': 'A', 'active': False}, {'label': 'B', 'active': False}, {'label': 'C', 'active': False}])
    assert a is None

def test_weighted():
    assert 0.36 < weighted((0.5, 2), (0.1, 1)) < 0.37
