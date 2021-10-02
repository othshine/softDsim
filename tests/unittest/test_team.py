from math import floor
from typing import Tuple

import pytest

from app.src.domain.dataObjects import WorkPackage
from app.src.domain.team import SkillType, Member, NotAValidSkillTypeException, Team, MemberIsHalted
from utils import YAMLReader


def test_skill_type_reads_parameter_from_yaml():
    t = 'senior'
    sl = SkillType(t)
    data = YAMLReader.read('skill-levels', t)
    assert sl.salary == data['salary']
    assert sl.error_rate == data['error-rate']
    assert sl.throughput == data['throughput']


def test_skill_type_raises_exception():
    with pytest.raises(NotAValidSkillTypeException):
        SkillType('not-a-skill-type')


def test_member_has_skill_type():
    m1 = Member(skill_type='junior')
    assert m1.skill_type == SkillType('junior')


def test_member_has_all_params():
    x = 0.4
    y = 0.99
    z = 0.1
    m = Member(skill_type='expert', xp_factor=x, motivation=y, familiarity=z)

    assert m.skill_type == SkillType('expert')
    assert m.xp_factor == x
    assert m.motivation == y
    assert m.familiarity == z
    assert m.halted is False


def test_team_add_operator():
    team = Team()
    assert len(team.staff) == 0
    team += Member()
    assert len(team.staff) == 1
    team += Member()
    assert len(team.staff) == 2


def test_team_remove_member():
    team = Team()
    m1 = Member()
    m2 = Member()
    assert m1 not in team
    assert m2 not in team
    team += m1
    team += m2
    assert m1 in team
    assert m2 in team
    team -= m1
    assert m1 not in team
    assert m2 in team


def test_team_remove_member_that_is_not_in_team():
    team = Team()
    assert len(team) == 0
    team += Member()
    assert len(team) == 1
    team -= Member()
    assert len(team) == 1


def test_team_size():
    team = Team()
    assert len(team) == 0
    team += Member()
    assert len(team) == 1


def test_teams_motivation():
    team = Team()
    assert team.motivation == 0
    team += Member(motivation=0.10)
    team += Member(motivation=0)
    assert .05 >= team.motivation >= .05


def test_teams_salary():
    team = Team()
    salary = 0
    assert team.salary == salary
    team += Member(skill_type='expert')
    salary += YAMLReader.read('skill-levels', 'expert', 'salary')
    assert team.salary == salary
    team += Member(skill_type='senior')
    salary += YAMLReader.read('skill-levels', 'senior', 'salary')
    assert team.salary == salary
    team += Member(skill_type='expert')
    salary += YAMLReader.read('skill-levels', 'expert', 'salary')
    assert team.salary == salary


def test_member_efficiency():
    t = 'junior'
    m = Member(skill_type=t, xp_factor=1, motivation=1, familiarity=1)
    thr = YAMLReader.read('skill-levels', t, 'throughput')
    eff = 1 * thr  # 1 = (1 + 1 + 1) / 3
    assert m.efficiency == eff

    t = 'senior'
    m = Member(skill_type=t, xp_factor=0.5, motivation=1, familiarity=0)
    thr = YAMLReader.read('skill-levels', t, 'throughput')
    eff = 0.5 * thr
    assert m.efficiency == eff


def test_member_solve_tasks_returns_int_tuple():
    m = Member()
    assert isinstance(m.solve_tasks(0), Tuple)
    assert isinstance(m.solve_tasks(8)[0], int)


def test_member_solves_tasks_and_makes_errors():
    t = 'senior'
    time = 5
    m = Member(skill_type=t, xp_factor=0.5, motivation=1, familiarity=0)
    thr = YAMLReader.read('skill-levels', t, 'throughput')
    err = YAMLReader.read('skill-levels', t, 'error-rate')
    eff = 0.5 * thr
    num_t = floor(eff * time * YAMLReader.read('task-completion-coefficient'))
    num_e = round(num_t * err)
    assert m.solve_tasks(time) == (num_t, num_e)


def test_member_factors_are_between_zero_and_one():
    Member(xp_factor=0.5, motivation=1, familiarity=0)
    with pytest.raises(ValueError):
        Member(xp_factor=1.1)
    with pytest.raises(ValueError):
        Member(motivation=-0.1)
    with pytest.raises(ValueError):
        Member(familiarity=3000)
    with pytest.raises(ValueError):
        Member(motivation=0.2, familiarity=2, xp_factor=.1)


def test_team_solves_tasks():
    t = Team()
    m1 = Member(xp_factor=1, motivation=1, familiarity=1)
    m2 = Member(xp_factor=0.5, motivation=0.5, familiarity=0.5)
    t += m1
    t += m2

    t, e = t.solve_tasks(time=4)

    tm1, em1 = m1.solve_tasks(4)
    tm2, em2 = m2.solve_tasks(4)

    assert t == tm1 + tm2
    assert e == em1 + em2


def test_member_training():
    m = Member()
    xp1 = m.xp_factor
    m.train()
    xp2 = m.xp_factor
    assert xp1 < xp2


def test_team_solve_tasks_halted_member():
    t = Team()
    m = Member(xp_factor=1, motivation=1, familiarity=1)
    mh = Member(xp_factor=1, motivation=1, familiarity=1)
    mh.halt()
    t += m
    t += mh

    t, e = t.solve_tasks(time=4)

    tm1, em1 = m.solve_tasks(4)

    assert t == tm1
    assert e == em1


def test_halted_member_raises_exception_when_solve_tasks():
    m = Member()
    m.halt()
    with pytest.raises(MemberIsHalted):
        m.solve_tasks(8)


def test_team_meeting():
    t = Team()
    m = Member()
    t += m
    f1 = m.familiarity
    t.meeting(5)
    f2 = m.familiarity
    assert f1 < f2


def test_team_get_member_by_id():
    t = Team()
    t += Member(xp_factor=1)
    t += Member(skill_type='expert')
    m = Member(skill_type='senior', xp_factor=0.1, motivation=1, familiarity=0)
    _id = m.get_id()
    t += m
    t += Member(xp_factor=0)
    m2 = t.get_member(_id)
    assert m2.get_id() == m.get_id()
    assert m2.skill_type == m.skill_type
    assert m2.xp_factor == m.xp_factor
    assert m2.motivation == m.motivation
    assert m2.familiarity == m.familiarity

def test_team_count_types():
    t = Team()
    t += Member("junior")
    t += Member("senior")
    t += Member("senior")
    t += Member("junior")
    t += Member("expert")
    assert t.count("junior") == 2
    assert t.count("senior") == 2
    assert t.count("expert") == 1


def test_remove_weakest_member():
    t = Team()
    m1 = Member(skill_type='junior', xp_factor=0.1, motivation=1, familiarity=0)
    m2 = Member(skill_type='senior', xp_factor=1, motivation=1, familiarity=1)
    m3 = Member(skill_type='senior', xp_factor=0.1, motivation=1, familiarity=0)
    m4 = Member(skill_type='junior', xp_factor=1, motivation=1, familiarity=0)
    t += m1
    t += m2
    t += m3
    t += m4
    assert m1 in t
    assert m2 in t
    assert m3 in t
    assert m4 in t
    t.remove_weakest('senior')
    assert m1 in t
    assert m2 in t
    assert m3 not in t
    assert m4 in t
    t.remove_weakest('junior')
    assert m1 not in t
    assert m2 in t
    assert m3 not in t
    assert m4 in t


def test_quality_check():
    t = Team()
    t += Member('expert', xp_factor=1, motivation=1, familiarity=1)
    wr = t.work(WorkPackage(days=5, daily_meeting_hours=0, tasks=100, unidentified_errors=5, identified_errors=3, quality_check=True, error_fixing=False))
    assert wr.identified_errors == 5
    assert wr.unidentified_errors > 0
    assert wr.tasks_completed > 0
    assert wr.fixed_errors == 0

    wr = t.work(WorkPackage(days=5, daily_meeting_hours=0, tasks=5, unidentified_errors=0, identified_errors=4,
                            quality_check=True, error_fixing=True))
    assert wr.identified_errors == 0
    assert wr.tasks_completed == 5
    assert wr.fixed_errors == 4