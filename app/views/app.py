import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.views.util import serving_log

from mongo_models import MongoConnection, ScenarioMongoModel, UserMongoModel, ClickHistoryModel, MongoConnection

def connected(t):
    c = MongoConnection()
    return c.is_connected(t)



@login_required
def app(request, sid):
    serving_log('app', request)
    return render(request, "app/app.html")


@login_required
def index(request):
    serving_log('index', request)
    if not connected(500):
        return render(request, "app/dbfail.html")
    scenario_model = ScenarioMongoModel()
    user_model = UserMongoModel()
    sc = scenario_model.find_all_templates()
    s_list = []
    for scenario in sc:
        user_score_rank = user_model.get_user_ranking(str(scenario.id)).get(request.user.username, {})
        best_score = user_score_rank.get('score', "-")
        rank = user_score_rank.get('rank', "-")
        tries = user_model.get_num_tries(user=request.user.username, template_id=str(scenario.id))
        s_list.append({
            'name': scenario.name,
            'id': str(scenario.id),
            'tries': tries,
            'best_score': best_score,
            'rank': rank
        })
    context = {'scenarios': s_list}


    return render(request, "app/index.html", context)


@login_required
def create_new(request, sid):
    model = ScenarioMongoModel()
    hist_model = ClickHistoryModel()
    user_model = UserMongoModel()
    hist_id = hist_model.new_hist()
    mid = model.create(sid, user=request.user.username, history_id=hist_id)
    user_model.initiate_scenario(user=request.user.username, scenario_template_id=sid, scenario_id=mid, history_id=hist_id)
    return redirect('/s/' + str(mid))


def result_stats(request, sid):
    mongo = ScenarioMongoModel()
    s = mongo.get(sid)
    return render(request=request, template_name="app/result.html", context={'scenario': s})
