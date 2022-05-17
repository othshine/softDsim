import logging
from app.src.scenario import UserScenario
from app.src.team import ScrumTeam
from utils import data_get, get_active_label


def evaluate_decision(data, decision):
    decision.evaluate(data.get(decision.dtype))


def adjust_scrum_management(s, param):
    if isinstance(s.team, ScrumTeam):
        s.team.junior_master = param.get('Junior Scrum Master')
        s.team.senior_master = param.get('Senior Scrum Master')
        s.team.po = param.get('Product Owner')


def get_points(param, data):
    points = 0
    for row in data['button_rows']:
        for answer in row['answers']:
            if answer['active'] is True:
                points += answer['points']

    return points


def apply_changes(s: UserScenario, data: dict):
    if staff := data_get(data['numeric_rows'], 'staff'):
        s.team.adjust(staff.get('values'), s)
    if staff := data_get(data['numeric_rows'], 'Scrum Management'):
        adjust_scrum_management(s, staff.get('values'))
        # Scrum teams always do error checking:
        s.perform_quality_check = True
        s.error_fixing = True
    if isinstance(s.team, ScrumTeam):
        s.team.adjust([t for t in data['numeric_rows'] if "scrum team" in t.get('title').lower()], s)
    if q := data_get(data['button_rows'], 'Testing'):
        if data_get(q['answers'], 'Perform', attr='label').get('active'):
            s.perform_quality_check = True
    if q := data_get(data['button_rows'], 'Fix Bugs'):
        if data_get(q['answers'], 'Perform', attr='label').get('active'):
            s.error_fixing = True
    for action in data['button_rows']:
        s.actions.adjust(action)
        funcs = {'model': set_model}
        if func := funcs.get(action.get('title').lower()):
            func(s, get_active_label(action.get('answers')))

def set_model(s: UserScenario, model):
    s.model = model.lower()
    if not isinstance(s.team, ScrumTeam) and s.model == 'scrum':
        s.team = ScrumTeam()


def generate_object_id():
    pass


def serving_log(page: str, request):
    logging.info(f"Serving {page}.html for user {request.user.username}")