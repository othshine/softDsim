from abc import ABC
from dataclasses import dataclass
from typing import List, Optional
from deprecated import deprecated

from bson import ObjectId

from app.src.domain.dataObjects import WorkPackage, WorkResult, SimulationGoal
from app.src.domain.team import Team, Member
from utils import month_to_day, YAMLReader


@dataclass
class Answer:
    label: str
    active: bool = False
    points: int = 0

    @property
    def json(self):
        return {'label': self.label, 'active': self.active, 'points': self.points}


@dataclass
class TextBlock(object):
    header: str
    content: str

    @property
    def json(self):
        return {'header': self.header,
                'content': self.content}


class Decision(ABC):
    def __init__(self, **kwargs):
        self.text: List[TextBlock] = kwargs.get('text', None)
        self.continue_text: str = kwargs.get('continue_text', "Continue")
        self.points = kwargs.get('points', 0)
        self.active_actions: List[str] = kwargs.get('active_actions', [])

    @property
    def json(self):
        data = {'continue_text': self.continue_text,
                'points': self.points,
                'active_actions': self.active_actions}
        if self.text:
            data = {**data, 'text': [t.json for t in self.text]}
        return data

    def get_max_points(self):
        pass

    def eval(self, args):
        pass

    def add_text_block(self, header: str, content: str):
        t = TextBlock(header, content)
        if self.text:
            self.text.append(t)
        else:
            self.text = [t]


class AnsweredDecision(Decision):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.actions: List[Action] = [Action(**a) for a in kwargs.get('actions', []) or []]

    def add_button_action(self, title, answers):
        self.actions.append(Action(id=str(ObjectId()), title=title, typ='button', active=True, answers=answers))

    @property
    def json(self):
        return {**super().json, 'actions': [a.full_json for a in self.actions]}

    def eval(self, data):
        """
        Evaluates a decision.
        :param data: Vue object that contains user choices.
        :return: None
        """
        user_actions = data['button_rows']
        for action in self.actions:
            if user_answer_data := next((item for item in user_actions if item["id"] == action.id), None):
                user_answer = next((item['label'] for item in user_answer_data['answers'] if item["active"] is True),
                                   None)
                p = action.get_points(user_answer)
                self.points += p


class SimulationDecision(Decision):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.goal: SimulationGoal = kwargs.get('goal')
        self.max_points: int = kwargs.get('max_points', 0)

    @property
    def json(self):
        return {**super().json, 'goal': self.goal.json}

    def set_goal(self, goal: SimulationGoal):
        self.goal = goal

    def get_max_points(self) -> int:
        return self.max_points


class Action:
    def __init__(self, id, title: str, typ: str, active: bool = False, answers=None):
        self.id = id
        self.title = title
        self.typ = typ
        self.active = active
        self.answers: List[Answer] = []
        if answers:
            for answer in answers:
                self.answers.append(Answer(**answer))

    @property
    def json(self):
        return {'title': self.title, 'answers': self.format_answers(), 'id': self.id}

    @property
    def full_json(self):
        return {**self.json, 'id': self.id, 'typ': self.typ, 'answers': [a.json for a in self.answers]}

    def format_answers(self):
        ans = []
        for a in self.answers:
            ans.append({'label': a.label, 'active': a.active})
        return ans

    def get_points(self, value: str) -> int:
        """
        Returns the points for a answer. Value must be the string that is also the answers label.
        :param value: str: the answers text.
        :return: int: points for that answer.
        """
        if not value: value = ""
        for answer in self.answers:
            if answer.label.lower() == value.lower():
                return answer.points
        return 0


class ActionList:
    def __init__(self, json=None):
        self.actions: List[Action] = []
        if json:
            for action in json:
                self.actions.append(Action(**action))

    @property
    def json(self):
        return [a.full_json for a in self.actions]

    def get(self, id) -> Optional[Action]:
        for action in self.actions:
            if action.id == id:
                return action
        return None

    def scrap_actions(self):
        for id in YAMLReader.read('actions', 'button-rows'):
            a = Action(id, YAMLReader.read('actions', 'button-rows', id, 'title'), 'button')
            for label in YAMLReader.read('actions', 'button-rows', id, 'values'):
                a.answers.append(Answer(label, False))
            self.actions.append(a)

    def adjust(self, data):
        if self.get(data.get('id')):
            for answer in self.get(data.get('id')).answers:
                for actual in data.get('answers', []):
                    if actual.get('label') == answer.label:
                        answer.active = actual.get('active')


class Scenario:
    def __init__(self, **kwargs):
        if json := kwargs.get('json'):
            self.build(json)
        else:
            self.tasks_done = int(kwargs.get('tasks_done', 0) or 0)
            self.tasks_total = int(kwargs.get('tasks_total', 0) or 0)
            self.actual_cost = int(kwargs.get('actual_cost', 0) or 0)
            self.budget = int(kwargs.get('budget', 0) or 0)
            self.current_day = int(kwargs.get('current_day', 0) or 0)
            self.scheduled_days = int()
            self.counter = int(kwargs.get('counter', -1))
            self.decisions = kwargs.get('decisions', []) or []
            self.id = ObjectId(kwargs.get('id')) or ObjectId()
            self.desc = kwargs.get('desc', 0) or ""
            self.actions = kwargs.get('actions', ActionList())
            self.team = Team()
            self.name = kwargs.get("name", "DefaultName")
            self.user = kwargs.get('user')

    def __iter__(self):
        return self

    def __next__(self) -> Decision:
        if self.counter >= len(self.decisions) - 1:
            raise StopIteration
        self._eval_counter()
        return self.decisions[self.counter]

    def __len__(self) -> int:
        return len(self.decisions)

    def __eq__(self, other):
        if isinstance(other, Scenario):
            return self.id == other.id
        return False

    @property
    def json(self):
        d = {'tasks_done': self.tasks_done,
             'tasks_total': self.tasks_total,
             'decisions': [dec.json for dec in self.decisions],
             'actual_cost': self.actual_cost,
             'budget': self.budget,
             'counter': self.counter,
             'current_day': self.current_day,
             'scheduled_days': self.scheduled_days,
             'desc': self.desc,
             'team': self.team.json,
             '_id': str(self.id),
             'id': str(self.id),
             'name': self.name,
             'actions': self.actions.json,
             'user': self.user
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
                if (action := self.actions.get(a)) is not None:
                    json.append(action.json)
        else:
            for action in d.actions or []:
                json.append(action.json)
        return json

    def get_max_points(self) -> int:
        return sum([d.get_max_points() for d in self.decisions])

    def work(self, days, meeting):
        wp = WorkPackage(days=days, daily_meeting_hours=meeting)
        self._apply_work_result(self.team.work(wp))
        self.actual_cost += month_to_day(self.team.salary, days)
        self.current_day += days

    def _apply_work_result(self, wr: WorkResult):
        self.tasks_done += wr.tasks_completed

    def build(self, json):  # ToDo: Refactor. Use **
        self.__init__(tasks_done=json.get('tasks_done'),
                      tasks_total=json.get('tasks_total'),
                      scheduled_days=json.get('scheduled_days'),
                      actual_cost=json.get('actual_cost'),
                      current_day=json.get('current_day'),
                      budget=json.get('budget'),
                      id=json.get('_id'),
                      desc=json.get('desc'),
                      name=json.get('name'),
                      counter=json.get('counter'),
                      actions=ActionList(json=json.get('actions')),
                      user=json.get('user')
                      )

        for d in json.get('decisions') or []:
            self.add(build_decision(d))
        if t := json.get('team'):
            for m in t.get('staff'):
                member = Member(m.get('skill-type'), xp_factor=m.get('xp'), motivation=m.get('motivation'),
                                familiarity=m.get('familiarity'), id=m.get('_id'))
                if m.get('halted'):
                    member.halt()
                self.team += member

    def get_id(self) -> str:
        return str(self.id)

    def _eval_counter(self):
        """
        Increases the value of the counter by one of the current decision is done.
        """
        if self.counter == -1:
            self.counter = 0
            print("set")
        else:
            d = self.decisions[self.counter]
            if (not isinstance(d, SimulationDecision)) or (
                    isinstance(d, SimulationDecision) and d.goal.reached(tasks=self.tasks_done)):
                self.counter += 1
                print("yes")
            else:
                print("no")
        print("C", self.counter)

    def get_decision(self, nr: int = None) -> Decision:
        if not nr:
            nr = self.counter
        return self.decisions[nr]


def build_decision(d):
    if d.get('goal'):
        dec = SimulationDecision(goal=SimulationGoal(**d.get('goal')), active_actions=d.get('active_actions'))
    else:
        dec = AnsweredDecision(active_actions=d.get('active_actions'), actions=d.get('actions'))
    for t in d.get('text') or []:
        dec.add_text_block(t.get('header'), t.get('content'))
    dec.points = d.get('points', 0)

    return dec
