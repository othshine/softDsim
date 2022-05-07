from deprecated.classic import deprecated
from rest_framework import serializers
from django.db import models


@deprecated(reason="this serializer was used for testing, DONT USE THIS")
class ScoreCardSerializer(serializers.Serializer):
    """
    This serializer is used in ScenarioSerializer.
    """

    budget_limit = serializers.CharField()
    time_limit = serializers.CharField()
    quality_limit = serializers.CharField()
    budget_p = serializers.CharField()
    time_p = serializers.CharField()
    quality_k = serializers.CharField()


class ScenarioSerializer(serializers.Serializer):
    """
    This class is used to serialize a Scenario into a json format
    in order to send it to the client.

    This is used in app/api/scenario_view.py
    """

    name = serializers.CharField()
    budget = serializers.CharField()
    scheduled_days = serializers.CharField()

    tasks_easy = serializers.CharField()
    tasks_medium = serializers.CharField()
    tasks_hard = serializers.CharField()
    pred_c = serializers.CharField()
    id = serializers.CharField()
    scorecard = ScoreCardSerializer()
