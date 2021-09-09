from app.src.domain.decision_tree import Scenario, Decision, TextBlock
from app.src.domain.team import Member
from mongo_models import ScenarioMongoModel


def add():
    mongo = ScenarioMongoModel()
    scenario = Scenario(tasks_total=400, budget=4000000)
    scenario.add(Decision(text=[TextBlock("Welcome", "To the game.")], dtype='simulate'))
    scenario.team += Member('junior')

    return mongo.save(scenario)


if __name__ == "__main__":
    print(add())
    print(add())
