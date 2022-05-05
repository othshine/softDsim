from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers.scenario_config import ScenarioConfig, ScenarioConfigSerializer

from app.models.scenario_config import ScenarioConfig


@method_decorator(csrf_protect, name="dispatch")
class ScenarioConfigView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ScenarioConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            print("Invalid")
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request, id=None):
        if id:
            if str(id).isnumeric():
                item = ScenarioConfig.objects.get(id=id)
            else:
                item = ScenarioConfig.objects.get(name=id)
            serializer = ScenarioConfigSerializer(item)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        items = ScenarioConfig.objects.all()
        serializer = ScenarioConfigSerializer(items, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, id=None):
        item = ScenarioConfig.objects.get(id=id)
        serializer = ScenarioConfigSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(ScenarioConfig, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})
