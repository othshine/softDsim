from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from mongo_models import ScenarioMongoModel, UserMongoModel, ClickHistoryModel


@login_required
def app(request, sid):
    return render(request, "app/app.html")


@login_required
def index(request):
    scenario_model = ScenarioMongoModel()
    user_model = UserMongoModel()
    sc = scenario_model.find_all_templates()
    s_list = []
    for scenario in sc:
        best_score = user_model.get_best_score(user=request.user.username, template_id=scenario.id)
        tries = user_model.get_num_tries(user=request.user.username, template_id=scenario.id)
        s_list.append({
            'name': scenario.name,
            'id': scenario.id,
            'tries': tries,
            'best_score': best_score
        })
    context = {'scenarios': s_list}

    return render(request, "app/index.html", context)


@login_required
def create_new(request, sid):
    model = ScenarioMongoModel()
    hist_model = ClickHistoryModel()
    mid = model.create(sid, user=request.user.username, history_id=hist_model.new_hist())
    return redirect('/s/' + mid)


def result_stats(request, sid):
    mongo = ScenarioMongoModel()
    s = mongo.get(sid)
    return render(request=request, template_name="app/result.html", context={'scenario': s})
