""" import pytest
from bson import ObjectId

from app.src.domain.dataObjects import WorkPackage, WorkResult, SimulationGoal
from app.src.domain.team import Team, Member


def test_team_works():
    t = Team(str(ObjectId()))
    m = Member('expert', motivation=0.5, xp_factor=0, familiarity=0)
    t += m
    work_result = t.work(WorkPackage(5, 1, 100, 10, 0, False, False))
    assert isinstance(work_result, WorkResult)
    assert work_result.tasks_completed > 0


def test_member_familiarity_growth():
    t = Team(str(ObjectId()))
    m = Member('expert', motivation=0.5, xp_factor=0, familiarity=0)
    t += m
    fam_before = m.familiarity
    t.work(WorkPackage(5, 1, 100, 10, 0, False, False))
    assert m.familiarity > fam_before


def test_sim_goal_tasks():
    goal = SimulationGoal(tasks=100)
    assert goal.reached(tasks=0) is False
    assert goal.reached(tasks=100) is True
    assert goal.reached(tasks=99) is False
    assert goal.reached(tasks=-200) is False
    assert goal.reached(tasks=299) is True

def test_add_work_results():
    wr1 = WorkResult(tasks_completed=100, unidentified_errors=10, identified_errors=0, fixed_errors=4)
    wr2 = WorkResult(tasks_completed=50, unidentified_errors=2, identified_errors=1, fixed_errors=0)
    wrr = WorkResult(tasks_completed=150, unidentified_errors=12, identified_errors=1, fixed_errors=4)
    assert wr1 + wr2 == wrr

def test_add_equal_work_results():
    wr1 = WorkResult(tasks_completed=100, unidentified_errors=10, identified_errors=0, fixed_errors=4)
    wr2 = WorkResult(tasks_completed=50, unidentified_errors=2, identified_errors=1, fixed_errors=0)
    wrr = WorkResult(tasks_completed=150, unidentified_errors=12, identified_errors=1, fixed_errors=4)
    wr1 += wr2
    assert wr1 == wrr
 """