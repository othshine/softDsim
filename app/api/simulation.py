import logging
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from app.decorators.decorators import allowed_roles
from app.models.scenario_config import ScenarioConfig
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from app.models.team import Team
from app.models.template_scenario_model import TemplateScenario
from app.models.user_scenario import ScenarioState, UserScenario
from app.serializers.user_scenario import UserScenarioSerializer


# The allowed_roles decorator does not work with non class-based views
# we will need to adjust it or write a second decorator for
# function based views. TODO: check roles.
@api_view(["GET", "POST"])
def start_new_simulation(request):

    template_id = request.data.get("template-id")
    config_id = request.data.get("config-id")

    try:
        template = TemplateScenario.objects.get(id=template_id)
    except ObjectDoesNotExist:
        msg = f"'{template_id}' is not a valid template-scenario id. Must provide attribute 'template-id'."
        logging.error(msg)
        return Response(
            {"status": "error", "data": msg}, status=status.HTTP_404_NOT_FOUND
        )
    try:
        config = ScenarioConfig.objects.get(id=config_id)
    except ObjectDoesNotExist:
        msg = f"'{config_id}' is not a valid scenario-config id. Must provide attribute 'config-id'."
        logging.error(msg)
        return Response(
            {"status": "error", "data": msg}, status=status.HTTP_404_NOT_FOUND
        )

    try:
        team = Team()
        team.save()
        state = ScenarioState()
        state.save()
        user_scenario = UserScenario(
            user=request.user, template=template, config=config, team=team, state=state
        )
        user_scenario.save()
        serializer = UserScenarioSerializer(user_scenario)
    except Exception as e:
        msg = f"'{e.__class__.__name__}' occurred when creating user scenario"
        logging.error(msg)
        logging.debug(e)
        return Response(
            {"status": "error", "data": msg},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(
        {"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED
    )
