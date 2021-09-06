from dataclasses import dataclass
from math import floor, sqrt
from statistics import mean
from typing import List

from utils import YAMLReader, value_or_error

# ToDo: Finish logic in team. Then save team in DB.

inc = lambda x: min([x + 0.1, 1.0])  # ToDo: Find a fitting function that approaches 1


class Member:
    def __init__(self, skill_type: str = 'junior', xp_factor: float = 0., motivation: float = 0.,
                 familiarity: float = 0.):
        self.skill_type = SkillType(skill_type)
        self.xp_factor = value_or_error(xp_factor)
        self.motivation = value_or_error(motivation)
        self.familiarity = value_or_error(familiarity)
        self.halted = False

    @property
    def efficiency(self) -> float:
        """
        Efficiency of a Member. Throughput (of SkillType) * Mean of xp, motivation and familiarity.
        :return: float
        """
        return self.skill_type.throughput * mean([self.xp_factor, self.motivation, self.familiarity])

    def solve_tasks(self, time: float) -> (int, int):
        """
        Simulates a member solving tasks for <time> hours.
        :param time: Number of hours.
        :return: Tuple of (Number of tasks solved, Number of these tasks that have errors)
        """
        if self.halted:
            raise MemberIsHalted
        number_tasks = floor(self.efficiency * time * YAMLReader.read('task-completion-coefficient'))
        number_tasks_with_unidentified_errors = round(number_tasks * self.skill_type.error_rate)  # Introduce fatigue?
        return number_tasks, number_tasks_with_unidentified_errors

    def train(self):
        """
        Training a member increases it's xp factor.
        :return: float - new xp factor value
        """
        self.xp_factor = inc(self.xp_factor)
        return self.xp_factor

    def halt(self):
        """
        Sets halted value to True.
        :return: True - halted value
        """
        self.halted = True
        return self.halted


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

    def solve_tasks(self, time):
        num_tasks = 0
        num_errs = 0
        for member in self.staff:
            if not member.halted:
                t, e = member.solve_tasks(time)
                num_tasks += t
                num_errs += e
        return num_tasks, num_errs

    def meeting(self):
        """
        A meeting increases every members familiarity.
        :return: None
        """
        for member in self.staff:
            if not member.halted:
                member.familiarity = inc(member.familiarity)


@dataclass
class SkillType:
    """
    Represents a level of skill that a member can have. (Junior, Senior, Expert). A skill type object contains all
    relevant information on a particular skill type.
    """

    def __init__(self, name: str):
        self.name = name
        try:
            data = YAMLReader.read('skill-levels', self.name)
        except KeyError:
            raise NotAValidSkillTypeException
        self.salary = data['salary']
        self.error_rate = data['error-rate']
        self.throughput = data['throughput']


class NotAValidSkillTypeException(Exception):
    """Exception raised when a skill type is created with an invalid name."""


class MemberIsHalted(Exception):
    """Exception raised when a halted member is called to work."""
