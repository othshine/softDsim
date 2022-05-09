import logging
from rest_framework import serializers

from app.models.user_scenario import ScenarioState, UserScenario
from app.serializers.scenario_config import ScenarioConfigSerializer
from app.serializers.user_serializer import UserSerializer
from app.serializers.team import TeamSerializer


class ScenarioStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioState
        fields = ["counter", "cost", "day"]


class UserScenarioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    config = ScenarioConfigSerializer(read_only=True)
    state = ScenarioStateSerializer()

    class Meta:
        model = UserScenario
        fields = ["id", "user", "config", "state", "team", "model"]

    def create(self, validated_data):
        state = None
        if "state" in validated_data:
            nested_serializer = self.fields["state"]
            nested_data = validated_data.pop("state")
            logging.info(nested_data)
            state = nested_serializer.create(validated_data=nested_data)

        obj = super(UserScenarioSerializer, self).create(validated_data)
        if state:
            obj.state = state
            obj.save()
        return obj

    def update(self, instance, validated_data):
        if "state" in validated_data:
            nested_serializer = self.fields["state"]
            nested_instance = instance.state
            nested_data = validated_data.pop("state")
            nested_serializer.update(nested_instance, nested_data)
        return super(UserScenarioSerializer, self).update(instance, validated_data)
