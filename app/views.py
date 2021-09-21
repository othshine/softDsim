import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from app.forms import ScenarioNameForm, ScenarioEditForm, DecisionEditForm
from app.src.domain.decision_tree import Scenario, Decision
from app.src.domain.team import Member
from mongo_models import ScenarioMongoModel, NoObjectWithIdException
from utils import data_get


@login_required
def index(request):
    mongo = ScenarioMongoModel()
    sc = mongo.find_all()
    context = {'scenarios': [s.json for s in sc]}
    return render(request, "app/index.html", context)


def evaluate_decision(data, decision):
    decision.evaluate(data.get(decision.dtype))


def adjust_staff(s, staff):
    for t in ['junior', 'senior', 'expert']:
        while s.team.count(t) > staff.get(t):
            s.team.remove_weakest(t)
        while s.team.count(t) < staff.get(t):
            s.team += Member(t)


@login_required
def app(request, sid):
    return render(request, "app/app.html")


def get_points(param, data):
    points = 0
    for row in data['button_rows']:
        for answer in row['answers']:
            if answer['active'] is True:
                points += answer['points']

    return points


def apply_changes(s: Scenario, data: dict):
    if staff := data_get(data['numeric_rows'], 'staff'):
        adjust_staff(s, staff.get('values'))


@login_required
@csrf_exempt
def click_continue(request, sid):
    model = ScenarioMongoModel()
    s = model.get(sid)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        apply_changes(s, data)
        s.work(5, int(data['meetings']))
        d = next(s)
    context = {
        "continue_text": d.continue_text,
        "tasks_done": s.tasks_done,
        "tasks_total": s.tasks_total,
        "blocks": [],
        "cost": s.team.salary,
        "actual_cost": s.actual_cost,
        'button_rows': s.button_rows,
        'numeric_rows': [
            {
                'title': "staff",
                'values':
                    {
                        'junior': s.team.count('junior'),
                        'senior': s.team.count('senior'),
                        'expert': s.team.count('expert')
                    }
            }
        ]

    }
    for t in d.text:
        context.get('blocks').append({'header': t.header, 'text': t.content})
    model.update(s)
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
    if request.method == 'POST':
        form = ScenarioNameForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            s = Scenario(name=form.cleaned_data['name'])
            mongo = ScenarioMongoModel()
            mid = mongo.save(s)
            print("XXX")
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
            print(data)
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


def register_request(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserCreationForm()
    return render(request=request, template_name="app/register.html", context={"form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="app/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    return redirect('/')
