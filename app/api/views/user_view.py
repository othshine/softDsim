from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, status
from app.api.serializers.user_serializers import UserSerializer


@method_decorator(csrf_protect, name="dispatch")
class UsersView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminUser)

    def get(self, request, username=None, format=None):

        if username:
            user = User.objects.get(username=username)
            user = UserSerializer(user, many=False)
            return Response(user.data, status=status.HTTP_200_OK)

        users = User.objects.all()
        users = UserSerializer(users, many=True)

        return Response(users.data, status=status.HTTP_200_OK)

    def delete(self, requests, username=None, format=None):

        try:
            user_tuple = User.objects.filter(username=username).delete()

            return Response(
                {
                    "success": "User deleted successfully",
                    "user": {"username": username},
                },
                status=status.HTTP_200_OK,
            )

        except:
            return Response(
                {"error": "User was not deleted"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, username=None, format=None):
        user = User.objects.get(username=username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
