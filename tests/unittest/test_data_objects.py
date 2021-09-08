import pytest

from app.src.domain.dataObjects import WorkPackage, WorkResult
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
