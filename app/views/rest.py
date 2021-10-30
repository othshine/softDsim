import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import app.src.domain.history as history
from app.src.domain.decision_tree import SimulationDecision
from app.src.domain.scenario import UserScenario
from app.views.util import apply_changes
from mongo_models import ScenarioMongoModel, UserMongoModel


@login_required
@csrf_exempt
def click_continue(request, sid):
    model = ScenarioMongoModel()
    s = model.get(sid)
    print(s.model, s.team)
    if not isinstance(s, UserScenario) or s.user != request.user.username:
        return HttpResponse(status=403)

    if request.method == 'GET':
        context = {"hi": True}
        return HttpResponse(json.dumps(context), content_type="application/json")

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        apply_changes(s, data)
        history.write(s.history_id, data, s.counter)
        if isinstance(s.get_decision(), SimulationDecision) and data.get('advance'):
            s.work(5, int(data['meetings']))
        if s.counter >= 0:
            s.get_decision().eval(data)
        try:
            d = next(s)
            context = {
                "continue_text": d.continue_text,
                "tasks_done": s.tasks_done,
                "tasks_total": s.template.tasks_total,
                "blocks": [],
                "cost": s.team.salary,
                "budget": s.template.budget,
                "scheduled_days": s.template.scheduled_days,
                "current_day": s.current_day,
                "actual_cost": s.actual_cost,
                'button_rows': s.button_rows,
                'numeric_rows': s.numeric_rows,
                'meeting_planner': 'meeting-planner' in d.active_actions,
                'motivation': s.team.motivation,
                'familiarity': s.team.familiarity,
                'done': False,
                'scrum': s.model == 'scrum' and isinstance(s.get_decision(), SimulationDecision)
            }
            if s.current_wr:
                context['current_workday'] = {
                    'tasks': s.current_wr.tasks_completed,
                    'ident_errs': s.current_wr.identified_errors,
                    'ident_total': s.identified_errors,
                    'fixed_errs': s.current_wr.fixed_errors
                }
            for t in d.text or []:
                context.get('blocks').append({'header': t.header, 'text': t.content})
        except StopIteration:
            context = {'done': True}
            user_model = UserMongoModel()
            user_model.save_score(user=request.user.username, scenario=s.template.id, score=s.total_score())
        model.update(s)
        return HttpResponse(json.dumps(context), content_type="application/json")