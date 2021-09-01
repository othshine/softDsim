import os
from dataclasses import dataclass
from statistics import mean
from typing import List

from django.conf import settings

from utils import YAMLReader


class Member:
    def __init__(self, skill_type: str = 'junior', xp_factor: float = 0., motivation: float = 0.,
                 familiarity: float = 0.):
        self.skill_type = SkillType(skill_type)
        self.xp_factor = xp_factor
        self.motivation = motivation
        self.familiarity = familiarity
        self.halted = False


class Team:
    def __init__(self):
        self.staff: List[Member] = []

    def __iadd__(self, member: Member):
        self.staff.append(member)
        return self

    def __isub__(self, member: Member):
        try:
            self.staff.remove(member)
        except ValueError:
            pass  # Maybe find a good solution for what to do here.
        return self

    def __contains__(self, member: Member):
        return member in self.staff

    def __len__(self):
        return len(self.staff)

    @property
    def motivation(self):
        """
        The teams motivation. Is considered to be the average (mean) of each team members motivation. 0 if team has
        no staff. :return: float
        """
        return mean([m.motivation for m in self.staff] or [0])

    @property
    def salary(self):
        """
        The teams total monthly salary expenditures. The sum of all members' salary.
        :return: int
        """
        return sum([m.skill_type.salary for m in self.staff] or [0])


@dataclass
class SkillType:
    """
    Represents a level of skill that a member can have. (Junior, Senior, Expert). A skill type object contains all
    relevant information on a particular skill type.
    """
    def __init__(self, name: str, config_path=os.path.join(settings.BASE_DIR, 'parameter.yaml')):
        self.name = name
        yr = YAMLReader(config_path)
        try:
            data = yr.read('skill-levels', self.name)
        except KeyError:
            raise NotAValidSkillTypeException
        self.salary = data['salary']
        self.error_rate = data['error-rate']
        self.throughput = data['throughput']


class NotAValidSkillTypeException(Exception):
    """Exception raised when a skill type is created with an invalid name."""
