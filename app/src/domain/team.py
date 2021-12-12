from statistics import mean
from typing import List

from bson import ObjectId

from app.src.domain.dataObjects import WorkPackage
from utils import YAMLReader, value_or_error

from scipy.stats import poisson

TASK_COMPLETION_COEF = YAMLReader.read('task-completion-coefficient')
ERR_COMPLETION_COEF = YAMLReader.read('error-completion-coefficient')
TASKS_PER_MEETING = YAMLReader.read('tasks-per-meeting-coefficient')
DONE_TASKS_FAMILIARITY_IMPACT_FACTOR = YAMLReader.read('done-tasks-familiarity-impact-factor')
TRAIN_SKILL_INCREASE_AMOUNT = YAMLReader.read('train-skill-increase-amount')

STRESS_PER_OVERTIME = YAMLReader.read('stress', 'overtime')
STRESS_REDUCTION_PER_WEEKEND = YAMLReader.read('stress', 'weekend-reduction')



def inc(x: float, factor: float = 1.0):
    """
    Increase function for increasing member values (xp, motivation, familiarity). Currently just adds 0.1 with a
    limit of 1. :param x: current value  :return: float - x + 0.1
    """
    return min([x + (0.01 * factor), 1.0])  # ToDo: Find a fitting function that approaches 1


class Member:
    def __init__(self, skill_type: str = 'junior', xp_factor: float = 0., motivation: float = 0.,
                 familiarity: float = 0.1, stress: float = 0.3, familiar_tasks=0, id=None):
        self.skill_type = SkillType(skill_type)
        self.xp_factor = value_or_error(xp_factor, upper=float('inf'))
        self.motivation = value_or_error(motivation)
        self.stress = value_or_error(stress)
        self.familiarity = value_or_error(familiarity)
        self.familiar_tasks = int(value_or_error(familiar_tasks, upper=float('inf')))
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
            'stress': self.stress,
            'familiarity': self.familiarity,
            'familiar-tasks': self.familiar_tasks,
            'halted': self.halted,
            '_id': str(self.id)
        }

    @property
    def efficiency(self) -> float:
        """
        Efficiency of a Member. Mean of motivation and familiarity and 1 - stress.
        :return: float
        """
        return mean([self.motivation, self.familiarity])

    def solve_tasks(self, time: float, tq, coeff=TASK_COMPLETION_COEF, team_efficiency: float = 1.0) -> (int, int):
        """
        Simulates a member solving tasks for <time> hours.
        """
        number_tasks = self.get_number_of_tasks(coeff, team_efficiency, time)
        m = tq.solve(number_tasks, self)
        self.familiar_tasks += (number_tasks - m)  # ToDo This should be done in the task queue
        self.update_familiarity(tq.total_tasks_done_or_tested)

        # If there were less than n tasks in the queue to do the member will go over to testing and fixing
        if m > 0:
            m = tq.test(m, self)
            tq.fix(m, self)

    def fix_errors(self, time: float, tq, coeff=TASK_COMPLETION_COEF, team_efficiency: float = 1.0) -> (int, int):
        """
        Simulates a member fixing errors for <time> hours.
        """
        number_tasks = self.get_number_of_tasks(coeff, team_efficiency, time)
        m = tq.fix(number_tasks, self)

        # If there were less than n tasks in the queue to fix the member will go over to solving and testing
        if m > 0:
            m = tq.solve(m, self)
            tq.test(m, self)

    def test_tasks(self, time: float, tq, coeff=TASK_COMPLETION_COEF, team_efficiency: float = 1.0) -> (int, int):
        """
        Simulates a member testing tasks for <time> hours.
        """
        number_tasks = self.get_number_of_tasks(coeff, team_efficiency, time)
        m = tq.test(number_tasks, self)

        # If there were less than n tasks in the queue to test the member will go over to solving and fixing
        if m > 0:
            m = tq.solve(m, self)
            tq.fix(m, self)

    def get_number_of_tasks(self, coeff, team_efficiency, time):
        """Returns the number of tasks that a member can solve/test/fix for <time> hours."""
        if self.halted:
            raise MemberIsHalted()
        mu = time * mean([self.efficiency, team_efficiency]) * (self.skill_type.throughput + self.xp_factor) * coeff
        number_tasks = poisson.rvs(mu)
        return number_tasks

    def train(self, hours=1, delta=0):
        """
        Training a member increases it's xp factor.
        :return: float - new xp factor value
        """
        self.xp_factor += (hours * delta * TRAIN_SKILL_INCREASE_AMOUNT)/((1+self.xp_factor)**2)  # Divide by xp_factor^2 to make it grow less with increasing xp factor
        print(self.skill_type.throughput)
        print(self.xp_factor)
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

    def update_familiarity(self, total_tasks_done):
        if self.familiar_tasks == 0 or total_tasks_done == 0:
            self.familiarity = 0
        else:
            self.familiarity = self.familiar_tasks / total_tasks_done

    def increase_stress(self, amount):
        self.stress = max(min(self.stress + amount, 1), 0)


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
    def motivation(self) -> float:
        """
        The teams motivation. Is considered to be the average (mean) of each team members motivation. 0 if team has
        no staff. :return: float
        """
        return mean([m.motivation for m in self.staff] or [0])

    @property
    def familiarity(self) -> float:
        """
        The teams familiarity. Is considered to be the average (mean) of each team members familiarity. 0 if team has
        no staff. :return: float
        """
        return mean([m.familiarity for m in self.staff] or [0])

    @property
    def stress(self) -> float:
        """
        The teams stress. Is considered to be the average (mean) of each team members stress. 0 if team has
        no staff. :return: float
        """
        return mean([m.stress for m in self.staff] or [0])

    @property
    def salary(self):
        """
        The teams total monthly salary expenditures. The sum of all members' salary.
        :return: int
        """
        return sum([m.skill_type.salary for m in self.staff] or [0])

    def solve_tasks(self, time, tq):
        for member in self.staff:
            if not member.halted:
                member.solve_tasks(time, tq, team_efficiency=self.efficiency())

    def fix_errors(self, time, tq):
        for member in self.staff:
            if not member.halted:
                member.fix_errors(time, tq, team_efficiency=self.efficiency())

    def test_tasks(self, time, tq):
        for member in self.staff:
            if not member.halted:
                member.test_tasks(time, tq, team_efficiency=self.efficiency())

    def work(self, wp: WorkPackage, tq):
        total_meeting_h = wp.meeting_hours
        total_training_h = wp.training_hours
        for day in range(wp.days):
            if day % 5 == 0:  # Reduce stress on the weekends
                self.increase_stress(STRESS_REDUCTION_PER_WEEKEND)
            day_hours = wp.day_hours
            if total_training_h > 0:
                self.train(total_training_h)
                day_hours -= total_training_h
                total_training_h = 0
            if total_meeting_h > 0 and day_hours > 0:
                if total_meeting_h > day_hours:
                    self.meeting(day_hours, tq.total_tasks_done_or_tested)
                    total_meeting_h -= day_hours
                    day_hours = 0
                else:
                    self.meeting(total_meeting_h, tq.total_tasks_done_or_tested)
                    day_hours -= total_meeting_h
                    total_meeting_h = 0
            if day_hours > 0 and wp.error_fixing and not wp.quality_check:
                self.fix_errors(day_hours, tq)
            elif day_hours > 0 and wp.quality_check and not wp.error_fixing:
                self.test_tasks(day_hours, tq)
            elif day_hours > 0 and wp.error_fixing and  wp.quality_check:
                td = day_hours // 2
                self.fix_errors(day_hours-td, tq)
                self.test_tasks(td, tq)
            elif day_hours > 0:
                self.solve_tasks(day_hours, tq)
            self.increase_stress((wp.day_hours-8)*STRESS_PER_OVERTIME)

    def meeting(self, time, total_tasks_done):
        """
        A meeting increases the number of familiar tasks for every member.
        :return: None
        """
        for member in self.staff:
            missing = total_tasks_done - member.familiar_tasks
            new_familiar_tasks = min((TASKS_PER_MEETING * time), missing)
            member.familiar_tasks += new_familiar_tasks
            member.update_familiarity(total_tasks_done)

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
        return (n * (n - 1)) / 2

    def efficiency(self):
        """Returns the team's efficiency. Which increases as the number of communication channels grows."""
        c = self.num_communication_channels
        return 1 / (1 + (c / 20 - 0.05))

    def train(self, total_training_h):
        m = mean([member.skill_type.throughput for member in self.staff if not member.halted])
        for member in self.staff:
            delta = m - member.skill_type.throughput
            if delta > 0:
                member.train(total_training_h, delta)

    def increase_stress(self, amount):
        for member in self.staff:
            member.increase_stress(amount)


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

    @property
    def stress(self):
        return mean([t.stress for t in self.teams] or [0])

    def work(self, wp: WorkPackage, tq):
        for team in self.teams:
            team.work(wp, tq)

    def get_team(self, id):
        for t in self.teams:
            if t.id == id:
                return t
        return None

    def adjust(self, data):
        for team_data in data:
            team = self.get_team(team_data.get('id'))
            if team:
                team.adjust(team_data.get('values'))
            else:
                id = str(ObjectId())
                new_team = Team(id)
                team_data['id'] = id
                new_team.adjust(team_data.get('values'))
                self.teams.append(new_team)

        for team in self.teams:
            if team.id not in [t.get('id') for t in data]:
                self.teams.remove(team)


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
