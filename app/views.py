import json

from bson import ObjectId
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from app.src.domain.dataObjects import WorkPackage
from app.src.domain.decision_tree import Scenario, Decision
from app.src.domain.team import Member
from mongo_models import ScenarioMongoModel, NoObjectWithIdException
from utils import dots


def index(request):
    return render(request, "app/index.html")


def evaluate_decision(data, decision):
    decision.evaluate(data.get(decision.dtype))


def get_scenario_cookie() -> str:
    return "61392659574bdd0855cc45c8"


def adjust_staff(s, staff):
    for t in ['junior', 'senior', 'expert']:
        while s.team.count(t) > staff[t]:
            s.team.remove_weakest(t)
        while s.team.count(t) < staff[t]:
            s.team += Member(t)


@csrf_exempt
def click_continue(request):
    counter = int(request.GET.get("counter"))
    model = ScenarioMongoModel()
    s_id = request.COOKIES.get('scenario')
    if s_id is None:
        s_id = '613927888e8faa586c05644a'
    s = model.get(s_id)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        adjust_staff(s, data['staff'])
        print(data)
        s.apply_work_result(s.team.work(WorkPackage(5, int(data['meetings']))))


    d = s._decisions[0]  # ToDo: if decision is Done: next()
    context = {
        "continue_text": d.continue_text,
        "tasks_done": s.tasks_done,
        "tasks_total": s.tasks_total,
        "blocks": [],
        "staff": {
            "junior": dots(s.team.count('junior')),
            "senior": dots(s.team.count('senior')),
            "expert": dots(s.team.count('expert'))
        },
        "cost": s.team.salary,

    }
    for t in d.text:
        context.get('blocks').append({'header': t.header, 'text': t.content})
    print(context)
    model.update(s)
    return HttpResponse(json.dumps(context), content_type="application/json")


@csrf_exempt
def click_simulate(request):
    model = ScenarioMongoModel()
    s = model.get(get_scenario_cookie())

    if request.method == 'POST':
        pass

    d = s._decisions[0]
    context = {
        "continue_text": d.continue_text,
        "tasks_done": s.tasks_done,
        "tasks_total": s.tasks_total,
        "blocks": [],
        "staff": {
            "junior": dots(s.team.count('junior')),
            "senior": dots(s.team.count('senior')),
            "expert": dots(s.team.count('expert'))
        }
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
