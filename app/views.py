import json

from bson import ObjectId
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from app.src.domain.decision_tree import Scenario, Decision
from mongo_models import ScenarioMongoModel


def index(request):
    s = Scenario()
    s.add(Decision("This is Question number one"))
    return render(request, "app/index.html")


@csrf_exempt
def click_continue(request):
    if request.method == 'POST':
        print(request.body)
    counter = int(request.GET.get("counter"))
    model = ScenarioMongoModel()
    s = model.get(ObjectId("612baed001cb8bc5e9cb2cb8"))
    d = s._decisions[counter]
    context = {
        "continue_text": d.continue_text,
        "tasks": s.tasks,
        "blocks": []
    }
    for t in d.text:
        context.get('blocks').append({'header': t.header, 'text': t.content})

    return HttpResponse(json.dumps(context), content_type="application/json")
