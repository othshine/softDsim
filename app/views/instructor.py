import json

from bson.objectid import ObjectId
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from app.src.domain.history import History
from mongo_models import ClickHistoryModel


def review(request, hid):
    print(hid)
    model = ClickHistoryModel()
    data = model.get(ObjectId(hid))
    data = History(**data)
    print(data)
    return render(request, "app/instructor/review.html", {'history': data})
