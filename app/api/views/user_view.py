from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, status
from app.api.serializers.user_serializers import UserSerializer


@method_decorator(csrf_protect, name='dispatch')
class UsersView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        users = User.objects.all()

        users = UserSerializer(users, many=True)
        return Response(users.data, status=status.HTTP_200_OK)

    @api_view(['GET'])
    def getOne(self, username, format=None):

        user = User.objects.get(username=username)
        user = UserSerializer(user, many=False)
        return Response(user.data, status=status.HTTP_200_OK)

    def delete(self, requests, format=None):
        user = self.request.user

        try:
            user_tuple = User.objects.filter(id=user.id).delete()

            return Response({'success': 'User deleted successfully', "user":
                {"id": user.id, "username": user.username}}, status=status.HTTP_200_OK)

        except:
            return Response({'error': 'User was not deleted'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# class DeleteAccountView(APIView):
#     """
#     Deletes user in current session.
#     Just for admin use at the moment.
#     """
#     def delete(self, requests, format=None):
#         user = self.request.user
#
#         # todo philip: add try/catch
#         user_tuple = User.objects.filter(id=user.id).delete()
#
#         return Response({'success': 'User deleted successfully', "user":
#             {"id": user.id, "username": user.username}})
#
#
# class GetUsersView(APIView):
#
#
#     def get(self, request, format=None):
#         users = User.objects.all()
#
#         users = UserSerializer(users, many=True)
#         return Response(users.data)