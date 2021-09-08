import pytest

from app.src.domain.dataObjects import WorkPackage, WorkResult
from app.src.domain.team import Team, Member


def test_team_works():
    t = Team()
    t += Member('expert', motivation=0.5, xp_factor=1, familiarity=1)

    work_result = t.work(WorkPackage(5, 0))

    assert isinstance(work_result, WorkResult)
    assert work_result.tasks_completed > 0

