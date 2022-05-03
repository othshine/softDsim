from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models.management_goal_model import (
    ManagementGoal,
    TaskGoal,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.serializers.management_goal_serializers import (
    TaskGoalSerializer,
    ManagementGoalSerializer,
)


class TaskGoalView(APIView):
    def post(self, request):
        serializer = TaskGoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request, id=None):
        if id:
            item = TaskGoal.objects.get(id=id)
            serializer = TaskGoalSerializer(item)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        items = TaskGoal.objects.all()
        serializer = TaskGoalSerializer(items, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, id=None):
        item = TaskGoal.objects.get(id=id)
        serializer = TaskGoalSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(TaskGoal, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


class ManagementGoalView(APIView):
    def post(self, request):
        serializer = ManagementGoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request, id=None):
        if id:
            item = ManagementGoal.objects.get(id=id)
            serializer = ManagementGoalSerializer(item)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        items = ManagementGoal.objects.all()
        serializer = ManagementGoalSerializer(items, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, id=None):
        item = ManagementGoal.objects.get(id=id)
        serializer = ManagementGoalSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(ManagementGoal, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})
