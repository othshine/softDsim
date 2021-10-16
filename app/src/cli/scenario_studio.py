import os

from bson import ObjectId

from app.src.domain.dataObjects import SimulationGoal
from app.src.domain.decision_tree import AnsweredDecision, SimulationDecision
from app.src.domain.scenario import Scenario
from mongo_models import ScenarioMongoModel
from utils import _YAMLReader


def make():
    YAMLReader = _YAMLReader('test.yaml')
    data = YAMLReader.read()
    s = Scenario(name=data.get('name', "DefaultName"),
                 tasks_total=data.get('tasks_total', 0),
                 budget=data.get('budget', 10000),
                 desc=data.get('desc', ''),
                 scheduled_days=data.get('scheduled_days', 100),
                 id=ObjectId()
                 )
    for decision in data.get('decisions', []):
        kwargs = {}
        if ct := decision.get('continue_text'):
            kwargs['continue_text'] = ct
        if aa := decision.get('active_actions'):
            kwargs['active_actions'] = aa
        if n := decision.get('name'):
            kwargs['name'] = n
        if g := decision.get('goal'):
            d = SimulationDecision(**kwargs, goal=SimulationGoal(tasks=g.get('tasks')))
        else:
            d = AnsweredDecision(**kwargs)
            for action in decision.get('actions'):
                d.add_button_action(title=action.get('title', ''),
                                    answers=[{'label': key, 'points': action['answers'][key]} for key in action[
                                        'answers']], required=action.get('required'), hover=action.get('hover', ""))
        for tb in decision.get('text', []):
            d.add_text_block(tb.get('header', ''), tb.get('content', ''))
        s.add(d)
    mongo = ScenarioMongoModel()
    print(mongo.save_template(s))


if __name__ == "__main__":
    make()
