import json
import random

from bson.objectid import ObjectId
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from custom_user.models import User
from app.forms import (
    DecisionEditForm,
    ScenarioEditForm,
    ScenarioNameForm,
    UserAutomationForm,
)
from app.src.scenario_overview import ScenarioOverview
from app.src.decision_tree import Decision
from app.src.history import History
from app.src.scenario import Scenario
from mongo_models import (
    ClickHistoryModel,
    ScenarioMongoModel,
    NoObjectWithIdException,
    UserMongoModel,
)

PREFIX = "sose_"
SUFFIX = None
CSV_SEPARATOR = ";"

PASSWORD_LEN = 8


@staff_member_required
def review(request, sid):
    # Scenario
    scenario_model = ScenarioMongoModel()
    scenario = scenario_model.get(sid)

    # History
    history_model = ClickHistoryModel()
    history = history_model.get(ObjectId(scenario.history_id))
    history = History(**history)

    # User
    user_model = UserMongoModel()
    ranking = user_model.get_user_ranking(scenario.template.id)
    ranking = [ranking.get(u).get("score") for u in ranking]
    ranking.sort()
    i = 1
    for score in ranking:
        if score > scenario.total_score():
            i += 1
        else:
            break

    return render(
        request,
        "app/instructor/review.html",
        {
            "history": history,
            "scenario": scenario,
            "ranking": i,
            "ranks": len(ranking) + 1,
        },
    )


@staff_member_required
def instructor_(request):
    overview = create_scenario_template_inspection_overview_all()
    return render(request, "app/instructor/instructor.html", {"overviews": overview})


def create_scenario_template_inspection_overview_all():
    overview = []
    model = ScenarioMongoModel()
    for scenario in model.find_all_templates():
        overview.append(create_scenario_template_inspection_overview(scenario))
    return overview


def create_scenario_template_inspection_overview(scenario):
    user_model = UserMongoModel()
    ranking = user_model.get_user_ranking(scenario.id)
    ranking = [ranking.get(u).get("score") for u in ranking]
    ranking.sort(reverse=True)
    if len(ranking) == 0:
        ranking.append(0)
    return ScenarioOverview(
        scenario_id=scenario.id,
        scenario_name=scenario.name,
        best_score=ranking[0],
        score_median=ranking[int(len(ranking) / 2)],
        score_75=ranking[int(len(ranking) * 0.25)],
        score_90=ranking[int(len(ranking) * 0.1)],
        users=ranking[0:3],
        avg_time=10,
        total_tries=user_model.get_num_total_tries(scenario.id),
        total_users=len(ranking),
    )


@staff_member_required
def instructor_inspect(request, sid):
    model = ScenarioMongoModel()
    try:
        overview = create_scenario_template_inspection_overview(model.get(sid))
        user_model = UserMongoModel()
        ranking = user_model.get_user_ranking(sid)
        return render(
            request,
            "app/instructor/inspect.html",
            {"overview": overview, "ranking": ranking},
        )
    except NoObjectWithIdException:
        return HttpResponseRedirect("/instructor")


@staff_member_required
def inpect_user(request, sid, username):
    history_model = UserMongoModel()
    scenario_model = ScenarioMongoModel()
    user_score_data = history_model.get_user_scorecard(user=username, template_id=sid)
    name = scenario_model.get(sid).name
    return render(
        request,
        "app/instructor/inspect_user.html",
        {
            "user_data": user_score_data,
            "name": name,
            "username": username,
            "tries": len(user_score_data),
        },
    )


def login(request):
    return render(request, "app/instructor/login.html")


@staff_member_required
def instructor_search(request):
    return render(request, "app/instructor/search.html")


@staff_member_required
@csrf_exempt
def scenarios(request):
    model = ScenarioMongoModel()
    if request.method == "POST":
        x = json.loads(request.body.decode("utf-8"))
        s = Scenario(json=x)
        model.save(s)
        return HttpResponse(status=201)
    else:
        x = model.find_all_templates()
        context = {"scenarios": [s.json for s in x]}
        return HttpResponse(json.dumps(context), content_type="application/json")


@staff_member_required
def scenario_search_result(request):
    return render(request, "app/instructor/search_result.html")


@csrf_exempt
def get_scenario(request, sid):
    model = ScenarioMongoModel()
    if request.method == "DELETE":
        try:
            x = model.remove(sid)
            return HttpResponse(status=200)
        except NoObjectWithIdException:
            return HttpResponse(status=404)
    return HttpResponse(
        json.dumps(model.get(sid).json), content_type="application/json"
    )


@staff_member_required
def add_scenario(request):
    if request.method == "POST":
        form = ScenarioNameForm(request.POST)
        if form.is_valid():
            s = Scenario(name=form.cleaned_data["name"])
            mongo = ScenarioMongoModel()
            mid = mongo.save(s)
            return HttpResponseRedirect(
                "/instructor/edit/" + s.get_id(),
            )  # ToDo: use reverse.
    context = {
        "form": ScenarioNameForm(),
        "info": "To create a new Scenario start by defining a name.",
        "header": "Add Scenario",
        "url": "/instructor/add/scenario",
        "btntext": "Create Scenario",
        "snippets": ["app/snippets/basic_form.html"],
    }
    return render(request, "app/instructor/instructor_edit.html", context)


@staff_member_required
def edit(request, sid):
    mongo = ScenarioMongoModel()
    s = mongo.get(sid)

    if request.method == "POST":
        form = ScenarioEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            s.budget = float(data.get("budget"))
            s.tasks_total = int(data.get("tasks"))
            mongo.update(s)
    context = {
        "form": ScenarioEditForm(
            {"name": s.name, "tasks": s.tasks_total, "budget": s.budget}
        ),
        "info": "Edit values of the Scenario.",
        "header": "Edit Scenario",
        "url": "/instructor/edit/" + sid,
        "btntext": "Save",
        "snippets": [
            "app/snippets/basic_form.html",
            "app/snippets/add_decision_btn.html",
        ],
    }
    return render(request, "app/instructor/instructor_edit.html", context)


@staff_member_required
def add_decision(request, sid):
    mongo = ScenarioMongoModel()
    s = mongo.get(sid)
    nr = len(s)
    s.add(Decision())
    mongo.update(s)
    return HttpResponseRedirect("/instructor/edit/" + sid + "/" + str(nr))


@staff_member_required
def edit_decision(request, sid, nr):
    mongo = ScenarioMongoModel()
    d = mongo.get(sid).get_decision(int(nr))

    context = {
        "form": DecisionEditForm({"continue_text": d.continue_text}),
        "info": "Edit values of the decision.",
        "header": "Edit Decision",
        "url": "/instructor/edit/" + sid,
        "btntext": "Save",
        "btn_url": "instructor/edit/" + sid + "/" + str(nr),
        "snippets": ["app/snippets/basic_form.html", "app/snippets/add_text_btn.html"],
    }
    return render(request, "app/instructor/instructor_edit.html", context)


@csrf_exempt
def create_users(request):
    if request.method == "POST":
        form = UserAutomationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            csv = ""
            sep = (
                CSV_SEPARATOR
                if data.get("csv_separator") == ""
                else data.get("csv_separator")
            )
            for i in range(int(data.get("number", 0))):
                username = data.get("prefix", PREFIX) + f"{i + 1:03d}"
                if data.get("suffix"):
                    username += data.get("suffix")
                password = create_password()
                User.objects.create_user(username=username, password=password)
                csv += username + sep + password + "\n"

            return HttpResponse(csv, content_type="text/csv")

    context = {
        "form": UserAutomationForm(),
    }
    return render(request, "app/instructor/user_creation.html", context)


def create_password():
    chars = "qwertzuiopasdfghjkyxcvbnmQWERTZUPASDFGHJKLYXCVBNM123456789"
    password = ""
    for i in range(PASSWORD_LEN):
        password += chars[random.randint(0, len(chars) - 1)]
    return password
