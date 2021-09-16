import pytest

from app.src.domain.dataObjects import SimulationGoal
from app.src.domain.decision_tree import Scenario, Decision, AnsweredDecision, SimulationDecision, TextBlock, Answer
from utils import YAMLReader


def test_scenario_get_next_decision():
    s = Scenario()
    s.add(AnsweredDecision())
    s.add(SimulationDecision(goal=SimulationGoal(tasks=350), max_points=200, points=100, continue_text="Week",
                             text=[TextBlock(header="a", content="b"), TextBlock(header='c', content='y')]))
    s.add(AnsweredDecision(answers=[Answer(points=100, text="Hi"), Answer(points=0, text="Lo")],
                           text=[TextBlock(header="x", content="cont"), TextBlock(header='abc', content='3')], points=5,
                           continue_text="CC"))

    d = next(s)

    assert isinstance(d, Decision)
    assert isinstance(d, AnsweredDecision)
    assert not isinstance(d, SimulationDecision)
    assert len(d) == 0
    assert d.points == 0
    assert d.continue_text == "Continue"

    def check():
        d = next(s)

        assert isinstance(d, Decision)
        assert not isinstance(d, AnsweredDecision)
        assert isinstance(d, SimulationDecision)
        assert d.goal == SimulationGoal(tasks=350)
        assert "a" in [t.header for t in d.text]
        assert "c" in [t.header for t in d.text]
        assert "b" in [t.content for t in d.text]
        assert "y" in [t.content for t in d.text]
        assert d.continue_text == "Week"
        assert d.points == 100
        assert d.get_max_points() == 200

    check()
    check()
    s.tasks_done = 349
    check()

    s.tasks_done = 350
    d = next(s)

    assert isinstance(d, Decision)
    assert isinstance(d, AnsweredDecision)
    assert not isinstance(d, SimulationDecision)

    assert "x" in [t.header for t in d.text]
    assert "abc" in [t.header for t in d.text]
    assert "cont" in [t.content for t in d.text]
    assert "3" in [t.content for t in d.text]
    assert d.continue_text == "CC"
    assert d.points == 5
    assert d.get_max_points() == 100
    assert "Hi" in [a.text for a in d.answers]
    assert "Lo" in [a.text for a in d.answers]

    with pytest.raises(StopIteration):
        next(s)


def test_scenario_loads_yaml_actions():
    s = Scenario()
    s.actions.add('model-pick')

    s.actions.load()

    j = s.actions.json
    assert j['button_rows'][0]['title'] == "Model"
