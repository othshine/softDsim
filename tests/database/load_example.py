from app.src.domain.dataObjects import SimulationGoal
from app.src.domain.decision_tree import Scenario, AnsweredDecision, Answer, SimulationDecision
from mongo_models import ScenarioMongoModel


def load():
    mongo = ScenarioMongoModel()
    s = Scenario(name="Lets See pt III")
    s.actions.scrap_actions()

    d = AnsweredDecision()
    d.add_text_block("Welcome", "Text data.")
    d.add_button_action(title='Model', answers=[{'label': "Waterfall", 'points': 100}, {'label': "Spiral", 'points': 0}, {'label': "Scrum", 'points': 0}])
    d.add_button_action(title='Education', answers=[{'label': "None", 'points': 100}, {'label': "Offer in leisure time", 'points': 0},
                                                {'label': "Offer while work", 'points': 0}])
    s.add(d)

    d = AnsweredDecision()
    d.add_text_block("Header 2", "Text data 2.")
    d.add_text_block("Header 3", "Text data 3.")
    d.active_actions.append('salary-pick')
    d.active_actions.append('life-cycle-pick')
    s.add(d)
    print(len(s))

    d = SimulationDecision(goal=SimulationGoal(tasks=400), max_points=250)
    d.add_text_block(header="Hi", content="lo")
    d.add_text_block(header="Last Block", content="Ready after 400 Tasks are reached")
    s.add(d)
    return mongo.save_template(s)


if __name__ == '__main__':
    print(load())
