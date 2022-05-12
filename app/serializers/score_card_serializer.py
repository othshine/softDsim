from rest_framework import serializers

from app.models.simulation_models.score_card_model import ScoreCard


class ScoreCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreCard
        fields = ("easy", "medium", "hard")
