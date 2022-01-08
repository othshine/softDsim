from bson import ObjectId

from app.src.domain.dataObjects import SimulationGoal
from app.src.domain.decision_tree import SimulationDecision, AnsweredDecision, ActionList
from app.src.domain.scenario import Scenario, UserScenario
from app.src.domain.task_queue import TaskQueue
from app.src.domain.task import Task
from app.src.domain.team import Member, Team


def parse_team(t, s):
    i = t.get('id') or str(ObjectId())
    team = Team(i)
    for m in t.get('staff'):
        member = Member(m.get('skill-type'), xp_factor=m.get('xp'), motivation=m.get('motivation'),
                        stress=m.get('stress'), familiarity=m.get('familiarity'),
                        familiar_tasks=m.get('familiar-tasks', 0), id=m.get('_id'), scenario=s, team=team)
        if m.get('halted'):
            member.halt()
        team += member
    return team

def create_task_queue(easy: int, medium: int, hard:int) -> TaskQueue:
    tq = TaskQueue()
    tq.add({Task(difficulty=d) for d in [*[1]*easy, *[2]*medium, *[3]*hard]})
    return tq


class _Factory:

    def deserialize(self, json, typ: str):
        if typ.lower() == "scenario":
            return self._create_scenario(json)
        if typ.lower() == "userscenario":
            return self._create_user_scenario(json)

    def create_user_scenario(self, user: str, template: dict, history_id: ObjectId) -> UserScenario:
        template = self.deserialize(template, 'scenario')
        us = UserScenario(user=user, id=ObjectId(), scenario=template, decisions=template.decisions, history=history_id,
                          tq=create_task_queue(easy=template.tasks_easy, medium=template.tasks_medium,
                                               hard=template.tasks_hard))
        us.actions.scrap_actions()
        return us

    def _create_scenario(self, data):
        s = Scenario(name=data.get('name', "DefaultName"),
                     tasks_easy=data.get('tasks_easy', 0),
                     tasks_medium=data.get('tasks_medium', 0),
                     tasks_hard=data.get('tasks_hard', 0),
                     budget=data.get('budget', 10000),
                     desc=data.get('desc', ''),
                     scheduled_days=data.get('scheduled_days', 100),
                     id=data.get('_id') or ObjectId()
                     )
        self._add_decisions(data.get('decisions', []), s)
        return s

    def _create_user_scenario(self, json) -> UserScenario:
        us = UserScenario(task_queue=json.get('task_queue'),
                          actual_cost=json.get('actual_cost'),
                          current_day=json.get('current_day'),
                          id=json.get('_id'),
                          counter=json.get('counter'),
                          actions=ActionList(json=json.get('actions')),
                          user=json.get('user'),
                          scenario=json.get('template'),
                          errors=json.get('errors'),
                          identified_errors=json.get('identified_errors'),
                          model=json.get('model'),
                          history=json.get('history'))
        if us.model.lower() == "scrum":
            if t := json.get('team'):
                if t := t.get('teams'):
                    for team in t:
                        us.team.teams.append(parse_team(team, us))
        else:
            if t := json.get('team'):
                us.team = parse_team(t, us)
        self._add_decisions(json.get('decisions', []), us)

        return us

    def _add_decisions(self, data, s):
        """
        Adds als decisions that are included in the list data in json (dict) format to the scenario typ object s.
        :param data: A list with decisions in json format (as python dicts).
        :param s: A Scenario or UserScenario typ of object.
        """
        for decision in data:
            kwargs = {}
            if ct := decision.get('continue_text'):
                kwargs['continue_text'] = ct
            if aa := decision.get('active_actions'):
                kwargs['active_actions'] = aa
            if n := decision.get('name'):
                kwargs['name'] = n
            if p := decision.get('points'):
                kwargs['points'] = p
            if g := decision.get('goal'):
                d = SimulationDecision(**kwargs, goal=SimulationGoal(tasks=g.get('tasks')))
            else:
                d = AnsweredDecision(**kwargs)
                for action in decision.get('actions'):
                    d.add_button_action(title=action.get('title', ''), id=action.get('id', ObjectId()),
                                        answers=[{'label': a['label'], 'points': a['points']} for a in
                                                 action['answers']], required=action.get('required'),
                                        hover=action.get('hover', ""))
            for tb in decision.get('text', []):
                d.add_text_block(tb.get('header', ''), tb.get('content', ''))
            s.add(d)


Factory = _Factory()
