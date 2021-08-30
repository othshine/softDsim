import pytest

from app.src.domain.decision_tree import Scenario, Decision, Answer
from mongo_models import ScenarioMongoModel, NoObjectWithIdException


def test_mongo_scenario_can_be_saved_loaded_and_deleted():
    mongo = ScenarioMongoModel()
    s = Scenario(budget=100000, scheduled_days=40, tasks=300)
    s2 = Scenario(budget=215, scheduled_days=677, tasks_total=2, tasks_done=30, current_day=30, actual_cost=300000, counter=4)

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
    d = Decision()
    d.add_text_block("Title", "This is some sweet content!")
    d.add(Answer(text="Kanban", points=30))
    d.add(Answer(text="Scrum", points=100))
    s.add(d)
    mid = mongo.save(s)

    result = mongo.get(mid)

    answers = [a.text for a in next(result).answers]
    assert "Kanban" in answers
    assert "Scrum" in answers


def test_mongo_scenario_saves_text_blocks():
    mongo = ScenarioMongoModel()
    s = Scenario()
    d = Decision()
    d.add_text_block("Title", "This is some sweet content!")
    d.add_text_block("Title 2", "C2")
    d.add(Answer(text="Kanban", points=30))
    d.add(Answer(text="Scrum", points=100))
    s.add(d)
    mid = mongo.save(s)

    result = mongo.get(mid)

    block = next(result).text[1]
    assert "Title 2" == block.header
    assert "C2" == block.content


def test_decision_saves_dtype_and_points():
    mongo = ScenarioMongoModel()
    s = Scenario()
    d = Decision(points=200)
    d.add_text_block("Title", "This is some sweet content!")
    d.add_text_block("Title 2", "C2")
    d.add(Answer(text="Kanban", points=30))
    d.add(Answer(text="Scrum", points=100))
    d.dtype = "model"
    s.add(d)
    mid = mongo.save(s)

    result = mongo.get(mid)

    dec = result._decisions[0]
    assert dec.dtype == "model"
    assert dec.points == 200