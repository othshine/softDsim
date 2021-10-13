import time
from math import floor
from statistics import mean
from typing import List

from bson import ObjectId

from app.src.domain.dataObjects import WorkPackage, WorkResult
from utils import YAMLReader, value_or_error, probability, weighted

TASK_COMPLETION_COEF = YAMLReader.read('task-completion-coefficient')
ERR_COMPLETION_COEF = YAMLReader.read('error-completion-coefficient')


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

    def solve_tasks(self, time: float, coeff=TASK_COMPLETION_COEF, team_efficiency:float=1.0) -> (int, int):
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
            number_tasks += probability(weighted((self.efficiency, 1), (team_efficiency, 1)) * coeff)
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
    def __init__(self, id: str):
        self.staff: List[Member] = []
        self.id = id

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
            'staff': [m.json for m in self.staff],
            'id': self.id
        }

    @property
    def motivation(self):
        """
        The teams motivation. Is considered to be the average (mean) of each team members motivation. 0 if team has
        no staff. :return: float
        """
        return mean([m.motivation for m in self.staff] or [0])

    @property
    def familiarity(self):
        """
        The teams familiarity. Is considered to be the average (mean) of each team members familiarity. 0 if team has
        no staff. :return: float
        """
        return mean([m.familiarity for m in self.staff] or [0])

    @property
    def salary(self):
        """
        The teams total monthly salary expenditures. The sum of all members' salary.
        :return: int
        """
        return sum([m.skill_type.salary for m in self.staff] or [0])

    def solve_tasks(self, time, err=False):
        num_tasks = 0
        num_errs = 0
        for member in self.staff:
            if not member.halted:
                if err:
                    t, e = member.solve_tasks(time, coeff=ERR_COMPLETION_COEF, team_efficiency=self.efficiency())
                else:
                    t, e = member.solve_tasks(time, team_efficiency=self.efficiency())
                num_tasks += t
                num_errs += e
        return num_tasks, num_errs

    def work(self, work_package: WorkPackage) -> WorkResult:
        wr = WorkResult()
        # print(work_package)
        t = 0
        e = 0
        for day in range(work_package.days):
            self.meeting(work_package.daily_meeting_hours)
            nt, ne = self.solve_tasks(work_package.daily_work_hours)
            t += nt
            e += ne
        wr.unidentified_errors += e
        if work_package.error_fixing:
            while t > 0 and wr.fixed_errors < work_package.identified_errors:
                t -= 1
                wr.fixed_errors += 1
        if work_package.quality_check:
            while t > 0 and wr.identified_errors < work_package.unidentified_errors:
                t -= 1
                wr.identified_errors += 1
        t_comp = min(t, work_package.tasks)
        wr.tasks_completed += t_comp
        while t - work_package.tasks >= 2:
            if wr.unidentified_errors > 0:
                wr.unidentified_errors -= 1
            t -= 2

        print("WEEK RESULT")
        print("Completed Tasks:", wr.tasks_completed)
        print("Fixed Errors:", wr.fixed_errors)
        print("Identified Errors:", wr.identified_errors)
        print("Unidentified Errors:", wr.unidentified_errors)

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

    def adjust(self, staff_data):
        for t in ['junior', 'senior', 'expert']:
            while self.count(t) > staff_data.get(t):
                self.remove_weakest(t)
            while self.count(t) < staff_data.get(t):
                self.staff.append(Member(t))

    @property
    def num_communication_channels(self):
        """Returns number of communication channels."""
        n = len(self.staff)
        return (n*(n-1))/2

    def efficiency(self):
        """Returns the team's efficiency. Which increases as the number of communication channels grows."""
        c = self.num_communication_channels
        return 1/(1+(c/20-0.05))


class ScrumTeam:
    def __init__(self, junior: int = 0, senior: int = 0, po: int = 0):
        self.teams: List[Team] = []
        self.junior_master = junior
        self.senior_master = senior
        self.po = po

    @property
    def json(self):
        return {
            'teams': [t.json for t in self.teams], 'junior_master': self.junior_master,
            'senior_master': self.senior_master, 'po': self.po
        }

    @property
    def salary(self):
        sal = sum([t.salary for t in self.teams])
        y = YAMLReader.read('manager')
        sal += y.get('junior').get('salary') * self.junior_master
        sal += y.get('senior').get('salary') * self.senior_master
        sal += y.get('po').get('salary') * self.po
        return sal

    @property
    def motivation(self):
        return sum([t.motivation for t in self.teams])

    @property
    def familiarity(self):
        return mean([t.familiarity for t in self.teams] or [0])

    def work(self, wp: WorkPackage) -> WorkResult:
        wr = WorkResult()
        for team in self.teams:
            wr += team.work(wp)
        return wr

    def get_team(self, id):
        for t in self.teams:
            if t.id == id:
                return t
        return None

    def adjust(self, data):
        for team_data in data:
            team = self.get_team(team_data.get('id'))
            if team:
                print("Team Adjusted:", team.id)
                team.adjust(team_data.get('values'))
            else:
                new_team = Team(str(ObjectId()))
                new_team.adjust(team_data.get('values'))
                self.teams.append(new_team)


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
