from dataclasses import dataclass, field
from random import random
from typing import Optional

from bson import ObjectId
from scipy.stats._discrete_distns import poisson

from app.src.domain.dataObjects import WorkPackage, WorkResult
from app.src.domain.decision_tree import ActionList, Decision, SimulationDecision
from app.src.domain.team import Team, ScrumTeam, Member
from utils import month_to_day, quality, YAMLReader

# Config Variables
STRESS_ERROR_INCREASE = YAMLReader.read('stress', 'error')


@dataclass
class Scenario:
    name: str
    budget: int
    scheduled_days: int
    decisions: list = field(default_factory=list)
    id: ObjectId = ObjectId()
    desc: str = ""
    tasks_easy: int = 0
    tasks_medium: int = 0
    tasks_hard: int = 0

    @property
    def tasks_total(self):
        return self.tasks_easy + self.tasks_medium + self.tasks_hard

    def add(self, decision):
        self.decisions.append(decision)

    @property
    def json(self):
        return {'name': self.name,
                'decisions': [dec.json for dec in self.decisions],
                'tasks_total': self.tasks_total,
                'tasks_easy': self.tasks_easy,
                'tasks_medium': self.tasks_medium,
                'tasks_hard': self.tasks_hard,
                'budget': self.budget,
                'scheduled_days': self.scheduled_days,
                '_id': str(self.id),
                'id': str(self.id),
                'desc': self.desc
                }


def create_staff_row(team: Team, title: str = 'staff'):
    return {
        'id': team.id,
        'title': f"{title}",
        'values':
            {
                'junior': team.count('junior'),
                'senior': team.count('senior'),
                'expert': team.count('expert')
            },
        'hover': "Juniors cost 3000/mo, have an error rate of 33% and have a throughput of 3 tasks. Seniors cost 4500/mo, have an error rate of 20% and have a throughput of 7 tasks. Experts cost 7000/mo, have an error rate of 5% and have a throughput of 7 tasks."
    }


class UserScenario:
    def __init__(self, **kwargs):
        self.identified_errors = int(kwargs.get('identified_errors', 0) or 0)
        self.task_queue = kwargs.get('tq') or TaskQueue(**kwargs.get('task_queue', {}))
        self.errors = int(kwargs.get('errors', 0) or 0)
        self.actual_cost = int(kwargs.get('actual_cost', 0) or 0)
        self.current_day = int(kwargs.get('current_day', 0) or 0)
        self.counter = int(kwargs.get('counter', -1))
        self.decisions = kwargs.get('decisions', []) or []
        self.id = ObjectId(kwargs.get('id')) or ObjectId()
        self.actions = kwargs.get('actions') or ActionList()
        self.user = kwargs.get('user')
        self.template: Scenario = kwargs.get('scenario')
        self.perform_quality_check = False
        self.error_fixing = False
        self.model = kwargs.get('model', 'waterfall') or ""
        self.history_id: ObjectId = kwargs.get('history')
        self.current_wr = None
        if self.model.lower() == 'scrum':
            self.team = ScrumTeam()
        else:
            self.team = Team(str(ObjectId()))

    def __iter__(self):
        return self

    def __next__(self) -> Decision:
        self._eval_counter()
        if self.counter >= len(self.decisions):
            raise StopIteration
        return self.decisions[self.counter]

    def __len__(self) -> int:
        return len(self.decisions)

    def __eq__(self, other):
        if isinstance(other, Scenario):
            return self.id == other.id
        return False

    @property
    def tasks_done(self) -> int:
        return self.task_queue.total_tasks_done

    @property
    def json(self):
        d = {'task_queue': self.task_queue.json,
             'errors': self.errors,
             'identified_errors': self.identified_errors,
             'decisions': [dec.json for dec in self.decisions],
             'actual_cost': self.actual_cost,
             'counter': self.counter,
             'current_day': self.current_day,
             'team': self.team.json,
             '_id': str(self.id),
             'id': str(self.id),
             'user': self.user,
             'actions': self.actions.json,
             'template_id': str(self.template.id),
             'model': self.model,
             'history': self.history_id
             }
        return d

    def add(self, decision: Decision):
        self.decisions.append(decision)

    def remove(self, index: int):
        del self.decisions[index]

    @property
    def button_rows(self):
        json = []
        d = self.decisions[self.counter]
        if isinstance(d, SimulationDecision):
            for a in d.active_actions or []:
                if (action := self.actions.get(a)) is not None and self.action_is_applicable(action):
                    json.append(action.json)
        else:
            for action in d.actions or []:
                json.append(action.json)
        return json

    @property
    def numeric_rows(self):
        json = []
        d = self.decisions[self.counter]
        for aa in d.active_actions:
            if aa == 'staff-pick':  # ToDo: Make this quick and dirty solution dynamic.
                if isinstance(self.team, Team):
                    json.append(create_staff_row(team=self.team))
                elif isinstance(self.team, ScrumTeam):
                    json.append({
                        'title': "Scrum Management",
                        'values':
                            {
                                'Junior Scrum Master': self.team.junior_master,
                                'Senior Scrum Master': self.team.senior_master,
                                'Product Owner': self.team.po
                            }
                    })
                    for i, team in enumerate(self.team.teams):
                        t = create_staff_row(team=team, title='Scrum Team')
                        json.append(t)

        return json

    def get_max_points(self) -> int:
        return sum([d.get_max_points() for d in self.decisions])

    def work(self, days, meeting, training, overtime):
        wp = WorkPackage(days=days, meeting_hours=meeting, training_hours=training,
                         quality_check=self.perform_quality_check,
                         error_fixing=self.error_fixing , day_hours=8 + overtime)
        wr = self.team.work(wp, self.task_queue)
        self.current_wr = wr
        self.actual_cost += month_to_day(self.team.salary, days)
        self.current_day += days

    def get_id(self) -> str:
        return str(self.id)

    def _eval_counter(self):
        """
        Increases the value of the counter by one of the current decision is done.
        """
        if self.counter == -1:
            self.counter = 0
        else:
            d = self.decisions[self.counter]
            if (not isinstance(d, SimulationDecision)) or (
                    isinstance(d, SimulationDecision) and d.goal.reached(tasks=self.task_queue.total_tasks_unit_tested)):
                self.counter += 1

    def get_decision(self, nr: int = None) -> Optional[Decision]:
        if nr is None:
            nr = self.counter
        if nr < 0:
            return None
        return self.decisions[nr]

    def get_answered_decisions(self):
        return [d for d in self.decisions if not isinstance(d, SimulationDecision)]

    def total_score(self) -> int:
        p = 0
        for d in self.decisions:
            p += d.points
        p += self.time_score()
        p += self.budget_score()
        p += self.task_queue.quality_score
        return p

    def time_score(self) -> int:
        # ToDo: use a defined factor instead of 100.
        # ToDo: the factor should have a weight that can be defined when create the scenario.
        return round((self.template.scheduled_days / self.current_day) * 100)

    def budget_score(self) -> int:
        if self.actual_cost == 0:
            return 0  # If no money was spent, something is wrong and the score is 0.
        return round((self.template.budget / self.actual_cost) * 100)

    def action_is_applicable(self, action):
        """Returns True if an action is applicable. Actions can have restrictions, e.g. model must be scrum or kanban.
        This function checks whether the action's restrictions are applicable in this scenario."""
        applicable = True
        if self.model.lower() not in [x.lower() for x in action.get_restrictions().get('model-pick', [self.model])]:
            applicable = False
        return applicable


class TaskQueue:  # Maybe rename in TaskQueueWrapper
    def __init__(self, easy=0, medium=0, hard=0):
        self.easy = self._to_tq(easy)
        self.medium = self._to_tq(medium)
        self.hard = self._to_tq(hard)

    def __len__(self) -> int:
        """Returns the total number of tasks. Any task with any status."""
        return len(self.easy) + len(self.medium) + len(self.hard)

    def __str__(self):
        return f'Easy:\n {self.easy}\nMedium:\n {self.medium}\nHard:\n {self.hard}'

    @property
    def total_tasks_todo(self) -> int:
        """Returns the total number of tasks to do."""
        return self.easy.todo + self.medium.todo + self.hard.todo

    def total_tasks_solved(self) -> int:
        """Returns the total number of tasks solved."""
        return self.easy.solved + self.medium.solved + self.hard.solved

    @property
    def total_tasks_done(self) -> int:
        """Returns the total number of tasks done. A done tasks is a task that has been solved but it is unknown if
        the tasks is solved or has an uniedentified error. done + solved + unidentified_error """
        return self.easy.done + self.medium.done + self.hard.done

    @property
    def total_tasks_unit_tested(self) -> int:
        """Returns the total number of tasks tested."""
        return self.easy.unit_tested + self.medium.unit_tested + self.hard.unit_tested

    @property
    def total_error_identified(self) -> int:
        """Returns the total number of identified errors."""
        return self.easy.error_identified + self.medium.error_identified + self.hard.error_identified

    @property
    def total_tasks_done_or_tested(self) -> int:
        """Returns the total number of tasks done or tested."""
        return self.total_tasks_done + self.total_tasks_unit_tested + self.total_error_identified

    @property
    def total_tasks_with_faults(self):
        return self.easy.tasks_with_faults + self.medium.tasks_with_faults + self.hard.tasks_with_faults
    
    @property
    def total_integration_tested(self):
        return self.easy.integration_tested + self.medium.integration_tested + self.hard.integration_tested

    def total_tasks(self):
        return len(self)

    @property
    def json(self) -> dict:
        """Returns a json representation of the Task Queue."""
        return {
            'easy': self.easy.json,
            'medium': self.medium.json,
            'hard': self.hard.json,
        }

    @property
    def quality_score(self):
        k = 8
        return int(((len(self) - self.total_tasks_with_faults) * 1/len(self))**k * 100)

    def solve(self, n, member: Member):
        """
        Member m solves n tasks of the queue. Juniors prefer easy>medium>hard tasks. Experts prefer
        hard>medium>easy tasks. And Seniors prefer medium tasks and will alternate between hard and easy after that.

        Function returns the number of tasks that were NOT solved because there were no more tasks in the queue.
        If all tasks were solved, the function therefore returns 0.
        """
        if member.skill_type.name == "junior":
            n = self.easy.solve(n, member)
            n = self.medium.solve(n, member, e=0.5)  # If a junior solves a medium tasks stress is increased by 50%
            n = self.hard.solve(n, member, e=1.0)  # If a junior solves a hard tasks stress is increased by 100%
        elif member.skill_type.name == "expert":
            n = self.hard.solve(n, member)
            n = self.medium.solve(n, member)
            n = self.easy.solve(n, member)
        elif member.skill_type.name == "senior":
            n = self.medium.solve(n, member)
            r = q = 0  # To make sure we dont end up in an infinite loop
            while n > 0 and (r == 0 or q == 0):
                r = self.hard.solve(1, member, e=0.75)  # If a senior solves a hard tasks stress is increased by 75%
                n -= (1 - r)
                if n > 0:
                    q = self.easy.solve(1, member)
                    n -= (1 - q)
        return n

    def test(self, n, member: Member):
        """
        Member m tests n errors in the queue.
        Juniors can only test easy tasks.
        Seniors can only test medium and easy tasks.
        Experts can test all tasks.

        Return number of tasks that were NOT used for testing because there were no more tasks in the queue.
        """
        if member.skill_type.name == "junior":
            n = self.easy.test(n, member)
        elif member.skill_type.name == "expert":
            n = self.hard.test(n, member)
            n = self.medium.test(n, member)
            n = self.easy.test(n, member)
        elif member.skill_type.name == "senior":
            n = self.medium.test(n, member)
            n = self.easy.test(n, member)

        return n

    def fix(self, n, member: Member):
        """
        Member m fixes n errors in the queue.
        Juniors can fix test easy tasks.
        Seniors can fix test medium and easy tasks.
        Experts can fix all tasks.

        Return number of tasks that were NOT used for fixing because there were no more tasks in the queue.
        """
        if member.skill_type.name == "junior":
            n = self.easy.fix(n, member)
        elif member.skill_type.name == "expert":
            n = self.hard.fix(n, member)
            n = self.medium.fix(n, member)
            n = self.easy.fix(n, member)
        elif member.skill_type.name == "senior":
            n = self.medium.fix(n, member)
            n = self.easy.fix(n, member)

        return n

    def _to_tq(self, arg):
        """Returns a _TaskQueue object from an int or a TQ in json form."""
        if isinstance(arg, int):
            return _TaskQueue(todo=arg)
        if isinstance(arg, _TaskQueue):
            return arg
        if isinstance(arg, dict):
            return _TaskQueue(**arg)
        raise ValueError('Invalid argument for TaskQueue')


class _TaskQueue:
    def __init__(self, todo: int = 0, solved: int = 0, error_unidentified: int = 0, error_identified: int = 0,
                 unit_tested: int = 0, integration_tested: int = 0):
        self.todo = todo
        self.solved = solved
        self.error_unidentified = error_unidentified
        self.error_identified = error_identified
        self.unit_tested = unit_tested
        self.integration_tested = integration_tested

    def __str__(self):
        return f'{self.todo} tasks to do, {self.solved} solved, {self.error_unidentified} unidentified errors, ' \
               f'{self.error_identified} identified errors, {self.unit_tested} tested, {self.integration_tested} integration_tested'

    def __len__(self):
        return self.todo + self.solved + self.error_unidentified + self.error_identified + self.unit_tested + self.integration_tested

    @property
    def done(self):
        return self.solved + self.error_unidentified

    @property
    def tasks_with_faults(self):
        """Returns the number of tasks that have faults. Every task that is not correclty solved is considered
        faulty. This number should not be readable by the team or a member but only be used for the calculation of
        the quality score. It can be unserstood as the number of all tasks that the customer finds faulty """
        return self.todo + self.error_unidentified + self.error_identified

    @property
    def json(self):
        """Returns a json representation of the Task Queue."""
        return {
            'todo': self.todo,
            'solved': self.solved,
            'error_unidentified': self.error_unidentified,
            'error_identified': self.error_identified,
            'tested': self.unit_tested,
            'integration_tested': self.integration_tested
        }

    def solve(self, n, member: Member, e: float = 0.0):
        """ Solves n tasks in the queue. If n is larger than the number of tasks in the queue, all tasks are solved. And
        the rest is returned."""
        # m is the number of tasks to solve, m is either equal to n or the number of tasks to do.
        m = min(n, self.todo)

        # Calculate the number of errors made
        mu_error = m * member.skill_type.error_rate * (member.stress + e)
        number_tasks_with_unidentified_errors = min(poisson.rvs(mu_error), m)

        # Adjust the numbers in the queue
        self.todo -= m
        self.solved += m - number_tasks_with_unidentified_errors
        self.error_unidentified += number_tasks_with_unidentified_errors
        member.stress = min(1, member.stress + number_tasks_with_unidentified_errors * STRESS_ERROR_INCREASE)

        # If all n tasks have been solved, return 0 else return the number of tasks that have not been solved (n - m)
        return n - m

    def test(self, n, member):
        # m is the number of tasks to test, m is either equal to n or the number of tasks to test (tasks done).
        m = min(n, self.done)

        for i in range(m):
            # Either the tested task is actually an error or it is not.
            # The probability of getting a tasks that is an error is:
            prob = self.error_unidentified / (self.error_unidentified + self.solved)
            if random() < prob:
                self.error_identified += 1
                self.error_unidentified -= 1
            else:
                self.solved -= 1
                self.unit_tested += 1
        return n - m

    def fix(self, n, member):
        # m is the number of tasks to fix, m is either equal to n or the number of tasks to fix (identified errors).
        m = min(n, self.error_identified)

        self.error_identified -= m
        self.unit_tested += m

        return n - m
