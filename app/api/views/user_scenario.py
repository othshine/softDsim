from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models.template_scenario_model import TemplateScenario
from app.serializers.user_scenario import UserScenarioSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from app.models.user_scenario import ScenarioState, UserScenario
from app.models.scenario_config import ScenarioConfig
from app.models.team import Team


@method_decorator(csrf_protect, name="dispatch")
class UserScenarioViews(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        errors = {}
        user = request.data.get("user")
        config = request.data.get("config")
        team = request.data.get("team")
        serializer = UserScenarioSerializer(data=request.data)
        template = request.data.get("template")
        try:
            template = TemplateScenario.objects.get(id=template)
        except ObjectDoesNotExist:
            errors[
                "template"
            ] = f"No template with id {template} does exist in Database. Template must be provided!"
        if user:
            try:
                user = User.objects.get(id=user)
            except ObjectDoesNotExist:
                errors["user"] = f"No user with id {user} does exist in Database."
        if config:
            try:
                config = ScenarioConfig.objects.get(id=config)
            except ObjectDoesNotExist:
                errors["config"] = f"No config with id {config} does exist in Database."
        if team:
            try:
                team = Team.objects.get(id=team)
            except ObjectDoesNotExist:
                errors["team"] = f"No team with id {team} does exist in Database."
        if errors:
            return Response(
                {"status": "error", "data": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.is_valid():
            obj = serializer.save()
            obj.template = template
            if user:
                obj.user = user
            if config:
                obj.config = config
            if team:
                obj.team = team
            obj.save()
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
            item = UserScenario.objects.get(id=id)
            serializer = UserScenarioSerializer(item)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        items = UserScenario.objects.all()
        serializer = UserScenarioSerializer(items, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, id=None):
        item = UserScenario.objects.get(id=id)
        user = request.data.get("user")
        config = request.data.get("config")
        team = request.data.get("team")
        errors = dict()
        if user:
            try:
                item.user = User.objects.get(id=user)
            except ObjectDoesNotExist:
                errors["user"] = f"No user with id {user} does exist in Database."
        if config:
            try:
                item.config = ScenarioConfig.objects.get(id=config)
            except ObjectDoesNotExist:
                errors["config"] = f"No config with id {config} does exist in Database."
        if team:
            try:
                item.team = Team.objects.get(id=team)
            except ObjectDoesNotExist:
                errors["team"] = f"No team with id {team} does exist in Database."
        if errors:
            return Response(
                {"status": "error", "data": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = UserScenarioSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(UserScenario, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})
