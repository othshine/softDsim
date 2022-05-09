from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializers.user_serializer import UserSerializer


@method_decorator(csrf_protect, name="dispatch")
class UserView(APIView):
    """
    `UserView` is the view for the user model, that implements basic CRUD
    functionality for users.
    These functions are called over the /api/user endpoint.
    The POST method to create a new user is in security_view in the register method.
    All functions in `UserView` are only available to an admin user.
    """

    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, username=None, format=None):
        """
        Method for GET-Requests to the /api/user endpoint.
        Retrieves users from the database.
        Returns one user if a username is specified as an url parameter (example: /api/user/Mario)
        Returns all users if no url parameter is given.

        Returns: Response with requested user/users and HTTP-Status Code
        """

        if username:
            user = User.objects.get(username=username)
            user = UserSerializer(user, many=False)
            return Response(user.data, status=status.HTTP_200_OK)

        users = User.objects.all()
        users = UserSerializer(users, many=True)

        return Response(users.data, status=status.HTTP_200_OK)

    def delete(self, requests, username=None, format=None):
        """
        Method for DELETE-Requests to the /api/user endpoint.
        Deletes user (in the database) that is specified as an url parameter (example: /api/user/Mario)

        Returns: Response with information about delete and HTTP-Status Code
        """
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
        """
        Method for PATCH-Requests to the /api/user endpoint.
        Updates User in database with information in json body.

        Returns: Response with updated user and HTTP-Status Code
        """
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
