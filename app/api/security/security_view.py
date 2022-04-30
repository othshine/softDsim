from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# from . import login_serializers

"""
Views for user authentication (login, logout, creation, csrf-token handling)
"""


# todo philip: add http status codes to responses

# not sure if needed
# @method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        is_authenticated = User.is_authenticated

        if is_authenticated:
            return Response({"isAuthenticated": "success"}, status=status.HTTP_200_OK)

        return Response({"isAuthenticated": "error"}, status=status.HTTP_403_FORBIDDEN)


@method_decorator(csrf_protect, name="dispatch")
class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        username = data["username"]
        password = data["password"]

        try:
            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": "Username already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.create_user(username=username, password=password)

            user.save()

            user = User.objects.get(id=user.id)

            return Response(
                {
                    "success": "User created successfully",
                    "user": {"id": user.id, "username": user.username},
                },
                status=status.HTTP_201_CREATED,
            )

        except:
            return Response(
                {"error": "Something went wrong (except clause)"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        # login is handled more by serializer - don't see benefit yet...
        # serializer = login_serializers.LoginSerializer(data=self.request.data, context={'request': self.request})
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        # login(request, user)

        data = self.request.data
        username = data["username"]
        password = data["password"]

        try:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return Response(
                    {"success": "User authenticated", "username": username},
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    {
                        "error": "Could not authenticate user - credentials might be wrong"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                {"error": "Something went wrong (except clause)"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    def post(self, request, formate=None):

        try:
            username = request.user.username
            logout(request)
            return Response(
                {"success": "Logged Out", "user": {"username": username}},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                {"error": "Logout failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({"success": "CSRF cookie set"}, status=status.HTTP_200_OK)


# X-CSRFToken:
# https://stackoverflow.com/questions/34782493/difference-between-csrf-and-x-csrf-token
# https://www.stackhawk.com/blog/django-csrf-protection-guide/
