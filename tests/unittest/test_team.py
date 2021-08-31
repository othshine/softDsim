import pytest
from yaml import load, dump, FullLoader

from app.src.domain.team import SkillType


def test_skill_level():
    t = 'senior'
    sl = SkillType(t)
    with open('../../parameter.yaml') as y:
        data = load(y, Loader=FullLoader)
        print(data)
        data = data['skill-levels'][t]

    assert sl.salary == data['salary']
    assert sl.error_rate == data['error-rate']
    assert sl.throughput == data['throughput']

def test_shit():
    assert 0 == 0