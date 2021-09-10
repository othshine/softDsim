import pytest

from app.src.domain.dataObjects import WorkPackage, WorkResult, SimulationGoal
from app.src.domain.team import Team, Member


def test_team_works():
    t = Team()
    m = Member('expert', motivation=0.5, xp_factor=0, familiarity=0)
    t += m
    work_result = t.work(WorkPackage(5, 1))
    assert isinstance(work_result, WorkResult)
    assert work_result.tasks_completed > 0


def test_member_familiarity_growth():
    t = Team()
    m = Member('expert', motivation=0.5, xp_factor=0, familiarity=0)
    t += m
    fam_before = m.familiarity
    t.work(WorkPackage(5, 2))
    assert m.familiarity > fam_before


def test_sim_goal_tasks():
    goal = SimulationGoal(tasks=100)
    assert goal.reached(tasks=0) is False
    assert goal.reached(tasks=100) is True
    assert goal.reached(tasks=99) is False
    assert goal.reached(tasks=-200) is False
    assert goal.reached(tasks=299) is True
