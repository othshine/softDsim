"""

"""
from app.src.domain.decision_tree import Scenario, Decision
from mongo_models import ScenarioMongoModel

PROMPT = "-> "


def build_decision():
    d = Decision()
    while _continue("adding Text Blocks"):
        print("New Text Block: ")
        h = input("Header: ")
        c = input("Content: ")
        d.add_text_block(h, c)
    d.dtype = input("Decision Type: ")
    if ask("Set Continue Button Text? "):
        d.continue_text = input("Text: ")

    while _continue("adding Answers"):
        d.add_answer(input("Text: "), int(input("Points: ")))

    return d


def ask(text):
    return not 'n' in input(text.strip() + " (n for no)? ").strip().lower()

def _continue(action=""):
    return ask("Continue "+action)


def build():
    params = {'tasks':0, 'budget':0, 'scheduled_days':0}

    for p in params:
        params.update({p:input("Set " + p + ":")})

    s = Scenario(tasks=params.get('tasks'), budget=params.get('budget'), scheduled_days=params.get('scheduled_days'))

    while _continue(action='creating decisions'):
        s.add(build_decision())

    model = ScenarioMongoModel()
    print("Scenario saved as " + str(model.save(obj=s)))


funcs = {
    'build': build
}


def read_command():
    args = input(PROMPT).strip().split(" ")
    f = funcs.get(args[0])
    if f:
        f()
    else:
        print(args[0], 'not a valid argument')


if __name__ == "__main__":
    while True:
        read_command()
