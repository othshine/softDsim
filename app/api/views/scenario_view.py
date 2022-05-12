from deprecated.classic import deprecated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializers.scenario_serializers import ScenarioSerializer
from mongo_models import ScenarioMongoModel


@deprecated(
    reason="this endpoint was only used for testing and is not needed in the final application"
)
@method_decorator(csrf_protect, name="dispatch")
class ScenarioView(APIView):
    """
    Views for Scenarios - WIP
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, scenario_id=None, format=None):

        if scenario_id:
            print(f"Getting scenario with id: {scenario_id}")

            # Get scenario from database
            scenario = ScenarioMongoModel().get(scenario_id)

            # serialize scenario using the ScenarioSerializer
            serializer = ScenarioSerializer(scenario)

            # return serialized scenario back to frontend
            data = {"scenario": serializer.data}

            return Response(
                data, status=status.HTTP_200_OK, content_type="application/json"
            )

        scenario_list = ScenarioMongoModel().find_all_templates()
        results = {str(s.id): s.name for s in scenario_list}
        data = {"count": len(results), "results": results}

        return Response(data, status=status.HTTP_200_OK)
