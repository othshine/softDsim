from app.models.scenario_config import ScenarioConfig
from rest_framework import serializers


class ScenarioConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioConfig
        fields = "__all__"
