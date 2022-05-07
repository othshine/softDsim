from rest_framework import serializers

from app.models.decision_models.answer_model import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("label", "points", "active")
