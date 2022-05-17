import json
import logging
from os import read

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import app.src.history as history
from app.src.decision_tree import SimulationDecision
from app.src.scenario import UserScenario
from app.views.util import apply_changes
from mongo_models import ScenarioMongoModel, UserMongoModel

from utils import data_get, get_active_label, read_button


# Todo move to a different file
def extract_overtime(param):
    return {
        'leave early': -1,
        '1 hour overtime': 1,
        '3 hours overtime': 3
    }.get(param, 0)


def end_scenario(s: UserScenario, username):
    context = {'done': True}
    user_model = UserMongoModel()
    user_model.save_score(user=username, scenario_template_id=s.template.id, score=s.total_score(),
                          scenario_id=str(s.id))
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
@csrf_exempt
def click_continue(request, sid):
    logging.info(f"Continue simulation for user {request.user.username}")
    model = ScenarioMongoModel()
    s = model.get(sid)
    tasks_done_before = len(s.task_queue.get(done=True))
    tasks_tested_before = len(s.task_queue.get(unit_tested=True))
    if not isinstance(s, UserScenario) or s.user != request.user.username:
        return HttpResponse(status=403)

    if request.method == 'GET':
        context = {"hi": True}
        return HttpResponse(json.dumps(context), content_type="application/json")

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if data.get('done', False):
            return end_scenario(s, request.user.username)
        apply_changes(s, data)
        history.write(s.history_id, data, s.counter)
        if isinstance(s.get_decision(), SimulationDecision) and data.get('advance'):
            try:
                integration_test = read_button(data, "Integration Test") == 'Scheduled'
                social_event = read_button(data, "Social Event") == 'Scheduled'
                training_hours = int(read_button(data, "Team Training Hours")[0])
                overtime = int(extract_overtime(read_button(data, "Overtime")))
            except:
                training_hours = 0
                overtime = 0

            s.work(5, int(data['meetings']), training_hours, overtime, integration_test=integration_test, social=social_event)
            logging.debug(f"Task Queue: {s.task_queue}")
        if s.counter >= 0:
            s.get_decision().eval(data)
        try:
            d = next(s)
            context = {
                "continue_text": d.continue_text,
                "tasks_done": len(s.task_queue.get(done=True)),
                "tasks_total": s.template.tasks_total,
                "blocks": [],
                "salaries": s.team.salary,
                "budget": s.template.budget,
                "scheduled_days": s.template.scheduled_days,
                "current_day": s.current_day,
                "actual_cost": s.actual_cost,
                'button_rows': s.button_rows,
                'numeric_rows': s.numeric_rows,
                'meeting_planner': 'meeting-planner' in d.active_actions,
                'motivation': s.team.motivation,
                'familiarity': s.team.familiarity,
                'stress': s.team.stress,
                'done': False,
                'scrum': s.model == 'scrum' and isinstance(s.get_decision(), SimulationDecision),
                "tasks": {
                    "todo": s.task_queue.size(done=False),
                    "done": s.task_queue.size(done=True),
                    "tested": s.task_queue.size(unit_tested=True),
                    "itested": s.task_queue.size(integration_tested=True),
                    "errors": s.task_queue.size(bug=True, unit_tested=True),
                    "done_week": s.task_queue.size(done=True) - tasks_done_before,
                    "tested_week": s.task_queue.size(unit_tested=True)- tasks_tested_before
                }
            }

            for t in d.text or []:
                context.get('blocks').append({'header': t.header, 'text': t.content})
        except StopIteration:
            model.update(s)
            return end_scenario(s, request.user.username)
        model.update(s)
        return HttpResponse(json.dumps(context), content_type="application/json")

def play(request, sid):
    model = UserMongoModel()
    r = model.get_user_ranking(sid)
    return HttpResponse(json.dumps(r), content_type="application/json")