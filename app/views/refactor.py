import json
import time

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from app.forms import ScenarioNameForm, ScenarioEditForm, DecisionEditForm
from app.src.domain.decision_tree import Decision, SimulationDecision
import app.src.domain.history as history
from app.src.domain.scenario import Scenario, UserScenario
from app.src.domain.team import Member, ScrumTeam
from mongo_models import ScenarioMongoModel, NoObjectWithIdException, UserMongoModel, ClickHistoryModel
from utils import data_get, get_active_label


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


def evaluate_decision(data, decision):
    decision.evaluate(data.get(decision.dtype))


def adjust_scrum_management(s, param):
    if isinstance(s.team, ScrumTeam):
        s.team.junior_master = param.get('Junior Scrum Master')
        s.team.senior_master = param.get('Senior Scrum Master')
        s.team.po = param.get('Product Owner')


@login_required
def app(request, sid):
    return render(request, "app/app.html")


@login_required
def create_new(request, sid):
    model = ScenarioMongoModel()
    hist_model = ClickHistoryModel()
    mid = model.create(sid, user=request.user.username, history_id=hist_model.new_hist())
    return redirect('/s/' + mid)


def get_points(param, data):
    points = 0
    for row in data['button_rows']:
        for answer in row['answers']:
            if answer['active'] is True:
                points += answer['points']

    return points


def apply_changes(s: UserScenario, data: dict):
    if staff := data_get(data['numeric_rows'], 'staff'):
        print(staff)
        s.team.adjust(staff.get('values'))
    if staff := data_get(data['numeric_rows'], 'Scrum Management'):
        adjust_scrum_management(s, staff.get('values'))
    if isinstance(s.team, ScrumTeam):
        print(data['numeric_rows'])
        s.team.adjust([t for t in data['numeric_rows'] if "scrum team" in t.get('title').lower()])
    if q := data_get(data['button_rows'], 'Quality Review'):
        if data_get(q['answers'], 'Perform', attr='label').get('active'):
            s.perform_quality_check = True
    if q := data_get(data['button_rows'], 'Fix Errors'):
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
        if isinstance(s.get_decision(), SimulationDecision):
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
            for t in d.text or []:
                context.get('blocks').append({'header': t.header, 'text': t.content})
        except StopIteration:
            context = {'done': True}
            user_model = UserMongoModel()
            user_model.save_score(user=request.user.username, scenario=s, score=s.total_score())
        model.update(s)
        return HttpResponse(json.dumps(context), content_type="application/json")


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


def result_stats(request, sid):
    mongo = ScenarioMongoModel()
    s = mongo.get(sid)
    return render(request=request, template_name="app/result.html", context={'scenario': s})
