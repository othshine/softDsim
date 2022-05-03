from rest_framework import serializers

from app.models.template_scenario_model import TemplateScenario


class TemplateScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateScenario
        fields = "__all__"
