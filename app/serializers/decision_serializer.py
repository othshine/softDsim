from rest_framework import serializers

from app.models.action_model import Action
from app.models.decision_models.decision_model import Decision
from app.models.text_block_model import TextBlock
from app.serializers.action_serializer import ActionSerializer
from app.serializers.text_block_serializer import TextBlockSerializer


class DecisionSerializer(serializers.ModelSerializer):

    text_block = TextBlockSerializer(many=True)
    action = ActionSerializer(many=True)

    class Meta:
        model = Decision
        fields = "__all__"

    def create(self, validated_data):
        text_data = validated_data.pop("text_block")
        actions_data = validated_data.pop("action")
        decision = Decision.objects.create(**validated_data)

        for data in text_data:
            TextBlock.objects.create(decision=decision, **data)

        for data in actions_data:
            Action.objects.create(decision=decision, **data)

        return decision
