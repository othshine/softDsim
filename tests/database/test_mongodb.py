import pytest

from app.src.domain.decision_tree import Scenario, Decision, Answer
from app.src.domain.team import Member, SkillType
from mongo_models import ScenarioMongoModel, NoObjectWithIdException


def test_mongo_scenario_update():
    mongo = ScenarioMongoModel()
    s = Scenario(budget=300)
    mid = mongo.save(s)
    result = mongo.get(mid)
    assert result == s
    assert result.budget == s.budget
    assert result.get_id() == s.get_id()
    assert len(result.team) == 0

    result.team += Member()
    result.current_day = 7

    mongo.update(result)

    result = mongo.get(mid)

    assert len(result.team) == 1
    assert result.current_day == 7
    assert result.budget == 300
    assert result.get_id() == s.get_id()


def test_mongo_scenario_can_be_saved_loaded_and_deleted():
    mongo = ScenarioMongoModel()
    s = Scenario(budget=100000, scheduled_days=40, tasks_done=300)
    s2 = Scenario(budget=215, scheduled_days=677, tasks_total=2, tasks_done=30, current_day=30, actual_cost=300000,
                  counter=4)

    mid = mongo.save(s)
    result = mongo.get(mid)
    assert result.budget == s.budget
    assert result.tasks_done == s.tasks_done
    assert result.counter == s.counter
    assert result == s

    mid2 = mongo.save(s2)
    result2 = mongo.get(mid2)
    assert result2.budget == s2.budget
    assert result2.current_day == s2.current_day
    assert result2 == s2

    mongo.remove(mid=mid)
    with pytest.raises(NoObjectWithIdException):
        mongo.get(mid)

    mid2 = mongo.update(result2)
    result3 = mongo.get(mid2)
    assert result2.get_id() == result3.get_id()
    assert result2.budget == s2.budget == result3.budget
    assert result2 == result3 == s2

    mongo.remove(mid=mid2)
    with pytest.raises(NoObjectWithIdException):
        mongo.get(mid2)


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
    a = Answer(text="Scrum", points=100)
    d.add(a)
    d.dtype = "model"
    s.add(d)
    mid = mongo.save(s)

    result = mongo.get(mid)

    dec = result._decisions[0]
    assert dec.dtype == "model"
    assert dec.points == 200
    assert dec.answers[0] == Answer(text='Scrum', points=100)
    assert dec.answers[0] != Answer(text='Kanban', points=0)
    assert dec.answers[0].json == a.json


def test_team_members_are_saved():
    mongo = ScenarioMongoModel()
    s = Scenario()
    s.team += Member(xp_factor=1, motivation=0.5, familiarity=0)

    mid = mongo.save(s)

    result = mongo.get(mid)
    team = result.team

    m = team.staff[0]

    assert m.xp_factor == 1
    assert m.motivation == 0.5
    assert m.familiarity == 0
    assert m.halted is False

    assert m.skill_type == SkillType('junior')


def test_halted_team_members_are_saved():
    mongo = ScenarioMongoModel()
    s = Scenario()
    m = Member()
    m.halt()
    s.team += m

    mid = mongo.save(s)

    result = mongo.get(mid)
    team = result.team

    m = team.staff[0]

    assert m.halted is True


def test_team_members_skill_type_are_saved():
    mongo = ScenarioMongoModel()
    s = Scenario()
    s.team += Member('senior')
    s.team += Member('expert')

    mid = mongo.save(s)

    result = mongo.get(mid)
    team = result.team

    stypes = [m.skill_type for m in team.staff]

    assert SkillType('senior') in stypes
    assert SkillType('expert') in stypes
    assert SkillType('junior') not in stypes


def test_member_id_is_same_when_saved():
    mongo = ScenarioMongoModel()
    s = Scenario()
    s.team += Member()
    m = Member(skill_type='senior', xp_factor=0.1, motivation=1, familiarity=0)
    _id = m.get_id()
    s.team += m
    s.team += Member(skill_type='senior')

    mid = mongo.save(s)
    result = mongo.get(mid)
    team = result.team

    m2 = team.get_member(_id)

    assert m2.get_id() == m.get_id()
    assert m2.skill_type == m.skill_type
    assert m2.xp_factor == m.xp_factor
    assert m2.motivation == m.motivation
    assert m2.familiarity == m.familiarity


def test_members_have_different_id():
    mongo = ScenarioMongoModel()
    s = Scenario()

    m1 = Member(skill_type='senior', xp_factor=0.1, motivation=1, familiarity=0)
    id1 = m1.get_id()
    s.team += m1

    m2 = Member(skill_type='expert', xp_factor=0.5, motivation=0, familiarity=0.099)
    id2 = m2.get_id()
    s.team += m2

    sid = mongo.save(s)

    result = mongo.get(sid)

    team = result.team

    m1n = team.get_member(id1)
    assert m1n.get_id() == m1.get_id()
    assert m1n.motivation == m1.motivation

    m2n = team.get_member(id2)
    assert m2n.get_id() == m2.get_id()
    assert m2n.motivation == m2.motivation
