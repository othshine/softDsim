from rest_framework import serializers

from app.models import Decision
from app.models.management_goal_model import ManagementGoal
from app.models.template_scenario_model import TemplateScenario
from app.serializers.decision_serializer import DecisionSerializer
from app.serializers.management_goal_serializers import ManagementGoalSerializer


class TemplateScenarioSerializer(serializers.ModelSerializer):
    management_goal = ManagementGoalSerializer()
    decision = DecisionSerializer(many=True)

    class Meta:
        model = TemplateScenario
        fields = ("id", "name", "management_goal", "decision")

    # create method for one to one field
    def create(self, validated_data):
        management_goal_data = validated_data.pop("management_goal")
        decision_data = validated_data.pop("decision")
        management_goal = ManagementGoal.objects.create(**management_goal_data)
        template_scenario = TemplateScenario.objects.create(
            management_goal=management_goal, **validated_data
        )
        for data in decision_data:
            Decision.objects.create(template_scenario=template_scenario, **data)

        return template_scenario
