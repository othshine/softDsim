from django.db import models
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from mongo_models import ScenarioMongoModel


@api_view(['GET'])
def scenario(req):
    scenario_list = ScenarioMongoModel().find_all_templates()
    results = {str(s.id): s.name for s in scenario_list}
    data = {'count': len(results), 'results': results}
    return Response(data, status=status.HTTP_200_OK)

