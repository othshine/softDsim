import pytest

from app.src.domain.decision_tree import Scenario, Decision, Answer
from mongo_models import ScenarioMongoModel, NoObjectWithIdException


def test_mongo_scenario_can_be_saved_loaded_and_deleted():
    mongo = ScenarioMongoModel()
    s = Scenario(budget=100000, scheduled_days=40, tasks=300)
    s2 = Scenario(budget=215, scheduled_days=677, tasks=2, current_day=30, actual_cost=300000, counter=4)

    mid = mongo.save(s)
    result = mongo.get(mid)
    assert result == s

    mid2 = mongo.save(s2)
    result2 = mongo.get(mid2)
    assert result2 == s2

    mongo.remove(obj=s)
    with pytest.raises(NoObjectWithIdException):
        mongo.get(mid)

    mid2 = mongo.save(s2)
    result2 = mongo.get(mid2)
    assert result2 == s2

    mongo.remove(mid=mid2)
    with pytest.raises(NoObjectWithIdException):
        mongo.get(mid)


def test_mongo_scenario_saves_decision_tree():
    mongo = ScenarioMongoModel()
    s = Scenario()
    d = Decision(text="This is a decision")
    d.add(Answer(text="Kanban", points=30))
    d.add(Answer(text="Scrum", points=100))
    s.add(d)
    mid = mongo.save(s)

    result = mongo.get(mid)
    print(result._decisions)

    answers = [a.text for a in next(result).answers]
    assert "Kanban" in answers
    assert "Scrum" in answers
