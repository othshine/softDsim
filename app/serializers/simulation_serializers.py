from rest_framework import serializers

from app.models.simulation_models.score_card_model import ScoreCard
from app.models.simulation_models.simulation_model import Simulation


class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = "__all__"


class ScoreCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreCard
        fields = "__all__"
