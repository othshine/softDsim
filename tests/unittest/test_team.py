import pytest

from app.src.domain.team import SkillType, Member, NotAValidSkillTypeException, Team
from utils import YAMLReader

yaml_reader = YAMLReader('../../parameter.yaml')


def test_skill_type_reads_parameter_from_yaml():
    t = 'senior'
    sl = SkillType(t)
    data = yaml_reader.read('skill-levels', t)
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
    y = 99
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
    team += Member(motivation=10)
    team += Member(motivation=0)
    assert 5. >= team.motivation >= 5.


def test_teams_salary():
    team = Team()
    salary = 0
    assert team.salary == salary
    team += Member(skill_type='expert')
    salary += yaml_reader.read('skill-levels', 'expert', 'salary')
    assert team.salary == salary
    team += Member(skill_type='senior')
    salary += yaml_reader.read('skill-levels', 'senior', 'salary')
    assert team.salary == salary
    team += Member(skill_type='expert')
    salary += yaml_reader.read('skill-levels', 'expert', 'salary')
    assert team.salary == salary
