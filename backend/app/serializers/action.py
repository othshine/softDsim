from rest_framework import serializers

from app.models.action import Action


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ("title", "typ", "lower_limit", "upper_limit")
