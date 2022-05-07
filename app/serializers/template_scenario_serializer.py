from django.shortcuts import get_object_or_404
from rest_framework import serializers

from app.models.decision_models.decision_model import Decision
from app.models.action_model import Action
from app.models.decision_models.answer_model import Answer
from app.models.management_goal_model import ManagementGoal
from app.models.template_scenario_model import TemplateScenario
from app.models.text_block_model import TextBlock
from app.serializers.decision_serializer import DecisionSerializer
from app.serializers.management_goal_serializers import ManagementGoalSerializer


class TemplateScenarioSerializer(serializers.ModelSerializer):
    management_goal = ManagementGoalSerializer()
    decisions = DecisionSerializer(many=True)

    class Meta:
        model = TemplateScenario
        fields = ("id", "name", "management_goal", "decisions")

    # create method for one to one field
    def create(self, validated_data, _id=None):

        # todo philip: add try/catch

        management_goal_data = validated_data.pop("management_goal")
        decision_data = validated_data.pop("decisions")

        # this if is when the create method gets called by the update method
        if _id:
            template_scenario = TemplateScenario.objects.create(
                id=_id, **validated_data
            )
        else:
            template_scenario = TemplateScenario.objects.create(**validated_data)

        management_goal = ManagementGoal.objects.create(
            template_scenario=template_scenario, **management_goal_data
        )

        for data in decision_data:

            text_block_data = data.pop("text_block")
            action_data = data.pop("actions")

            decision = Decision.objects.create(
                template_scenario=template_scenario, **data
            )

            for action in action_data:

                answers_data = action.pop("answers")

                action = Action.objects.create(decision=decision, **action)

                for answer in answers_data:
                    Answer.objects.create(action=action, **answer)

            for text_block in text_block_data:
                TextBlock.objects.create(decision=decision, **text_block)

        return template_scenario

    def update(self, instance, validated_data):

        instance_id = instance.id

        instance.delete()

        new_template_scenario = self.create(validated_data, instance_id)
        return new_template_scenario
