import json

from bson import ObjectId
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from app.src.domain.decision_tree import Scenario, Decision
from mongo_models import ScenarioMongoModel, NoObjectWithIdException


def index(request):
    return render(request, "app/index.html")


def evaluate_decision(data, decision):
    decision.evaluate(data.get(decision.dtype))


def get_scenario_cookie() -> ObjectId:
    return ObjectId("612d1a2c87b29722e1f39871")


@csrf_exempt
def click_continue(request):
    counter = int(request.GET.get("counter"))
    model = ScenarioMongoModel()
    s = model.get(get_scenario_cookie())

    if request.method == 'POST':
        evaluate_decision(json.loads(request.body.decode('utf-8')), s._decisions[counter - 2])

    d = s._decisions[counter]
    context = {
        "continue_text": d.continue_text,
        "tasks": s.tasks,
        "blocks": []
    }
    for t in d.text:
        context.get('blocks').append({'header': t.header, 'text': t.content})

    return HttpResponse(json.dumps(context), content_type="application/json")


def instructor(request):
    return render(request, "app/instructor/instructor.html")


def instructor_search(request):
    return render(request, "app/instructor/search.html")


@csrf_exempt
def scenarios(request):
    model = ScenarioMongoModel()
    if request.method == 'POST':
        x = json.loads(request.body.decode('utf-8'))
        s = Scenario(json=x)
        model.save(s)
        return HttpResponse(status=201)
    else:
        x = model.find_all()
        context = {'scenarios': [s.json for s in x]}
        return HttpResponse(json.dumps(context), content_type="application/json")


def scenario_search_result(request):
    return render(request, "app/instructor/search_result.html")

@csrf_exempt
def get_scenario(request, sid):
    model = ScenarioMongoModel()
    if request.method == 'DELETE':
        try:
            x = model.remove(mid=sid)
            return HttpResponse(status=200)
        except NoObjectWithIdException:
            return HttpResponse(status=404)
    return HttpResponse(json.dumps(model.get(sid).json), content_type="application/json")


def add_scenario(request):
    return render(request, "app/instructor/add_scenario.html")