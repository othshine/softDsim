from app.src.domain.dataObjects import SimulationGoal
from app.src.domain.decision_tree import Scenario, AnsweredDecision, Answer, SimulationDecision
from mongo_models import ScenarioMongoModel


def load():
    mongo = ScenarioMongoModel()
    s = Scenario(name="Lets See")
    s.actions.scrap_actions()

    d = AnsweredDecision()
    d.add_text_block("Welcome", "Text data.")
    d.active_actions.append('model-pick')
    s.add(d)

    d = AnsweredDecision()
    d.add_text_block("Header 2", "Text data 2.")
    d.add_text_block("Header 3", "Text data 3.")
    d.active_actions.append('salary-pick')
    d.active_actions.append('life-cycle-pick')
    s.add(d)

    d = SimulationDecision(goal=SimulationGoal(tasks=400), max_points=250)
    d.add_text_block(header="Hi", content="lo")
    s.add(d)
    return mongo.save(s)

if __name__ == '__main__':
    print(load())