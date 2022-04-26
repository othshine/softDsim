from django.db import models
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.auth import get_user_model


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

