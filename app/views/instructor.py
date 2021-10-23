import json

from bson.objectid import ObjectId
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app.forms import DecisionEditForm, ScenarioEditForm, ScenarioNameForm
from app.src.domain.decision_tree import Decision
from app.src.domain.history import History
from app.src.domain.scenario import Scenario
from mongo_models import ClickHistoryModel, ScenarioMongoModel, NoObjectWithIdException


def review(request, hid):
    print(hid)
    model = ClickHistoryModel()
    data = model.get(ObjectId(hid))
    data = History(**data)
    print(data)
    return render(request, "app/instructor/review.html", {'history': data})


def instructor_(request):
    return render(request, "app/instructor/instructor.html")


def instructor_search(request):
    return render(request, "app/instructor/search.html")


@csrf_exempt
def scenarios(request):
    model = ScenarioMongoModel()
    if request.method == 'POST':
        x = json.loads(request.body.decode('utf-8'))
        s = Scenario(json=x)
        model.save(s.json)
        return HttpResponse(status=201)
    else:
        x = model.find_all_templates()
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
    if request.method == 'POST':
        form = ScenarioNameForm(request.POST)
        if form.is_valid():
            s = Scenario(name=form.cleaned_data['name'])
            mongo = ScenarioMongoModel()
            mid = mongo.save(s.json)
            return HttpResponseRedirect("/instructor/edit/" + s.get_id(), )  # ToDo: use reverse.
    context = {
        'form': ScenarioNameForm(),
        'info': 'To create a new Scenario start by defining a name.',
        'header': 'Add Scenario',
        'url': '/instructor/add/scenario',
        'btntext': 'Create Scenario',
        'snippets': [
            'app/snippets/basic_form.html'
        ]
    }
    return render(request, "app/instructor/instructor_edit.html", context)


def edit(request, sid):
    mongo = ScenarioMongoModel()
    s = mongo.get(sid)

    if request.method == 'POST':
        form = ScenarioEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            s.budget = float(data.get('budget'))
            s.tasks_total = int(data.get('tasks'))
            mongo.update(s)
    context = {
        'form': ScenarioEditForm({'name': s.name, 'tasks': s.tasks_total, 'budget': s.budget}),
        'info': 'Edit values of the Scenario.',
        'header': 'Edit Scenario',
        'url': '/instructor/edit/' + sid,
        'btntext': 'Save',
        'snippets': [
            'app/snippets/basic_form.html',
            'app/snippets/add_decision_btn.html'
        ]
    }
    return render(request, "app/instructor/instructor_edit.html", context)


def add_decision(request, sid):
    mongo = ScenarioMongoModel()
    s = mongo.get(sid)
    nr = len(s)
    s.add(Decision())
    mongo.update(s)
    return HttpResponseRedirect("/instructor/edit/" + sid + "/" + str(nr))


def edit_decision(request, sid, nr):
    mongo = ScenarioMongoModel()
    d = mongo.get(sid).get_decision(int(nr))

    context = {
        'form': DecisionEditForm({'continue_text': d.continue_text}),
        'info': 'Edit values of the decision.',
        'header': 'Edit Decision',
        'url': '/instructor/edit/' + sid,
        'btntext': 'Save',
        'btn_url': 'instructor/edit/' + sid + "/" + str(nr),
        'snippets': [
            'app/snippets/basic_form.html',
            'app/snippets/add_text_btn.html'
        ]
    }
    return render(request, "app/instructor/instructor_edit.html", context)