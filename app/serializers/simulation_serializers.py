from deprecated.classic import deprecated
from rest_framework import serializers

from app.models.simulation_models.score_card_model import ScoreCard
from app.models.simulation_models.simulation_model import Simulation


@deprecated(reason="template_scenario_serializer is used now")
class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = "__all__"
