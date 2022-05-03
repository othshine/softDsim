from rest_framework import serializers

from app.models.decision_models.answer_model import Answer
from app.models.decision_models.decision_model import Decision


class DecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decision
        fields = "__all__"
