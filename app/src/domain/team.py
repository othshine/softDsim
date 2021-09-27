from math import floor
from statistics import mean
from typing import List

from bson import ObjectId

from app.src.domain.dataObjects import WorkPackage, WorkResult
from utils import YAMLReader, value_or_error, probability


# ToDo: Finish logic in team. Then save team in DB.

def inc(x: float):
    """
    Increase function for increasing member values (xp, motivation, familiarity). Currently just adds 0.1 with a
    limit of 1. :param x: current value  :return: float - x + 0.1
    """
    return min([x + 0.1, 1.0])  # ToDo: Find a fitting function that approaches 1


class Member:
    def __init__(self, skill_type: str = 'junior', xp_factor: float = 0., motivation: float = 0.,
                 familiarity: float = 0., id=None):
        self.skill_type = SkillType(skill_type)
        self.xp_factor = value_or_error(xp_factor)
        self.motivation = value_or_error(motivation)  # ToDo: Calculate Motivation.
        self.familiarity = value_or_error(familiarity)
        self.halted = False
        self.id = ObjectId() if id is None else ObjectId(id) if isinstance(id, str) else id

    def __eq__(self, other):
        if isinstance(other, Member):
            return self.id == other.id
        return False

    @property
    def json(self):
        return {
            'skill-type': self.skill_type.name,
            'xp': self.xp_factor,
            'motivation': self.motivation,
            'familiarity': self.familiarity,
            'halted': self.halted,
            '_id': str(self.id)
        }

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
        number_tasks = 0
        number_tasks_with_unidentified_errors = 0
        for _ in range(round(time)):
            number_tasks += probability(self.efficiency * YAMLReader.read('task-completion-coefficient'))
        for _ in range(number_tasks):
            number_tasks_with_unidentified_errors += probability(self.skill_type.error_rate)
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

    def get_id(self) -> ObjectId:
        return self.id


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
    def json(self):
        return {
            'staff': [m.json for m in self.staff]
        }

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

    def work(self, work_package: WorkPackage) -> WorkResult:
        wr = WorkResult()
        for day in range(work_package.days):
            self.meeting(work_package.daily_meeting_hours)
            nt, ne = self.solve_tasks(work_package.daily_work_hours)
            wr.tasks_completed += nt
            wr.unidentified_errors += ne
        return wr

    def meeting(self, time):
        """
        A meeting increases every members familiarity.
        :return: None
        """
        for member in self.staff:
            if not member.halted:
                for _ in range(time):  # ToDo: This can be included in the the improved inc function.
                    member.familiarity = inc(member.familiarity)

    def get_member(self, _id: ObjectId) -> Member:
        for m in self.staff:
            if m.get_id() == _id:
                return m
        raise ValueError

    def count(self, skill_type_name):
        """
        Returns the number of
        :param skill_type_name:
        :return:
        """
        c = 0
        for m in self.staff:
            if m.skill_type.name == skill_type_name:
                c += 1
        return c

    def remove_weakest(self, skill_type_name: str):
        w = None
        for m in self.staff:
            if m.skill_type.name == skill_type_name and (w is None or w.efficiency > m.efficiency):
                w = m
        self.__isub__(w)


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

    def __str__(self):
        return "SkillType: " + self.name

    def __eq__(self, other):
        if isinstance(other, SkillType):
            return other.name == self.name
        return False


class NotAValidSkillTypeException(Exception):
    """Exception raised when a skill type is created with an invalid name."""


class MemberIsHalted(Exception):
    """Exception raised when a halted member is called to work."""
