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
from app.models.team import Member, SkillType, Team
from app.models.template_scenario_model import TemplateScenario
from app.models.user_scenario import ScenarioState, UserScenario
from app.serializers.user_scenario import UserScenarioSerializer
from app.serializers.team import MemberSerializer


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


@api_view(["GET", "POST"])
def next_step(request):

    scenario = auth_user_scenario(request)
    if isinstance(scenario, Response):
        return scenario

    return Response(status=status.HTTP_200_OK)


@api_view(["GET", "POST", "DELETE"])
def adjust_team(request, id=None):
    scenario = auth_user_scenario(request)
    if isinstance(scenario, Response):
        return scenario
    if request.method == "POST":
        member_data = request.data.get("member")
        if str(member_data).isnumeric():
            skill_type = SkillType.objects.get(id=int(member_data))
        else:
            skill_type = SkillType.objects.get(name=member_data)
        member_obj = Member(team=scenario.team, skill_type=skill_type)
        member_obj.save()
        serializer = MemberSerializer(member_obj)
        return Response(
            data={"status": "success", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    if request.method == "GET":
        member_objs = Member.objects.filter(team=scenario.team)
        serializer = MemberSerializer(member_objs, many=True)
        return Response(
            data={"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK,
        )
    if request.method == "DELETE":
        try:
            member_to_delete = Member.objects.get(id=id)
            if member_to_delete.team == scenario.team:
                member_to_delete.delete()
                msg = f"Member with id {id} deleted."
                logging.info(msg)
                return Response(
                    data={"status": "success", "data": msg},
                    status=status.HTTP_200_OK,
                )
            else:
                msg = f"Member {id} does not belong to a team in user-scenario {scenario.id}"
                logging.warn(msg)
                return Response(
                    data={"status": "error", "data": msg},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except ObjectDoesNotExist:
            msg = f"Member with id {id} does not exist."
            logging.warn(msg)
            return Response(
                data={"status": "error", "data": msg}, status=status.HTTP_404_NOT_FOUND
            )

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def auth_user_scenario(request):
    """This functions can be used for each endpoint that deals with UserScenarios during
    a simulation. If the the scenario exists and the user is authorized to use it, the
    function returns the UserScenario object. If something is wrong, the function
    returns a Response object with a fitting description."""
    user = request.user
    scenario_id = request.data.get("scenario-id")
    if scenario_id is None:
        msg = "Attribute scenario-id must be provided"
        logging.error(msg)
        return Response({"status": "error", "data": msg}, status.HTTP_404_NOT_FOUND)

    try:
        scenario = UserScenario.objects.get(id=scenario_id)
    except ObjectDoesNotExist:
        msg = f"No UserScenario with id {scenario_id} found"
        logging.error(msg)
        return Response(
            {"status": "error", "data": msg}, status=status.HTTP_404_NOT_FOUND
        )

    if user.username == scenario.user.username:
        pass
    else:
        logging.warn(
            f"User {user.username} tried to access scenario {scenario_id} without permission."
        )
        return Response(
            {
                "status": "error",
                "data:": f"User {user.username} is not authorized to access scenario {scenario_id}",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return scenario