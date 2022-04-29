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

# not sure if needed
# @method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(APIView):

    def get(self, request, format=None):
        is_authenticated = User.is_authenticated

        if is_authenticated:
            return Response({'isAuthenticated': 'success'})

        return Response({'isAuthenticated': 'error'})


@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        try:
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'})

            user = User.objects.create_user(username=username, password=password)

            user.save()

            user = User.objects.get(id=user.id)

            return Response({'success': 'User created successfully', 'user': {
                "id": user.id, "username": user.username
            }})

        except:
            return Response({'error': 'Something went wrong (except clause)'})


@method_decorator(csrf_protect, name='dispatch')
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
        username = data['username']
        password = data['password']

        try:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return Response({'success': 'User authenticated', 'username': username})
            else:
                return Response({'error': 'Error Authenticating'})
        except:
            return Response({'error': 'Something went wrong (except clause)'})


# will be csrf protected because user is logged in
class LogoutView(APIView):

    def post(self, request, formate=None):
        try:
            logout(request)
            return Response({'success': 'Logged Out'})
        except:
            return Response({'error': 'Logout failed'})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})





# X-CSRFToken:
# https://stackoverflow.com/questions/34782493/difference-between-csrf-and-x-csrf-token


# https://www.guguweb.com/2022/01/23/django-rest-framework-authentication-the-easy-way/