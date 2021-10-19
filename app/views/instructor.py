import json

from bson.objectid import ObjectId
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from mongo_models import ClickHistoryModel


def review(request, hid):
    print(hid)
    model = ClickHistoryModel()
    data = model.get(ObjectId(hid))
    print(data)
    return render(request, "app/instructor/review.html", data)