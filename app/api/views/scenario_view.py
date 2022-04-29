import json

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from app.api.serializers.scenario_serializers import ScenarioSerializer
from mongo_models import ScenarioMongoModel


class ScenarioEndpoint(APIView):
    """
    Views for Scenarios - WIP
    """

    @api_view(['GET'])
    def scenario(req):
        scenario_list = ScenarioMongoModel().find_all_templates()
        results = {str(s.id): s.name for s in scenario_list}
        data = {'count': len(results), 'results': results}
        return Response(data, status=status.HTTP_200_OK)

    @api_view(['GET'])
    def get_one_scenario(req, id):
        print(f'Getting scenario with id: {id}')

        # Get scenario from database
        scenario = ScenarioMongoModel().get(id)

        # serialize scenario using the ScenarioSerializer
        serializer = ScenarioSerializer(scenario)

        # return serialized scenario back to frontend
        data = {'scenario': serializer.data}

        return Response(data, status=status.HTTP_200_OK, content_type="application/json")
