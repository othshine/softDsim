import json
from django.db import models
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.auth import get_user_model

from django.http import HttpRequest
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required


# @api_view(['GET'])
# def user_count(req):
#     user = get_user_model()
#     uc = user.objects.count()
#     return Response({"count": uc}, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_count(request):
    user = get_user_model()
    uc = user.objects.all()
    users = []
    for user in uc:
        users.append(user.username)
    return Response({"usernames": users}, status=status.HTTP_200_OK)



@api_view(["POST"])
def login(request: HttpRequest):
    request_body= request.data
    
    username= request_body.get("username")
    pw = request_body.get("password")


    user = authenticate(username=username, password=pw)

    if user:
        token = Token.objects.create(user=user)
        print(token.key)



@api_view(["GET"])
@login_required
def auth():
    return Response({"Hi": 100}, status=status.HTTP_200_OK)