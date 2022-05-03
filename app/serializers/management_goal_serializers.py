from rest_framework import serializers

from app.models.management_goal_model import TaskGoal, ManagementGoal


class TaskGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGoal
        fields = "__all__"


class ManagementGoalSerializer(serializers.ModelSerializer):
    tasks = TaskGoalSerializer()

    class Meta:
        model = ManagementGoal
        fields = ("id", "tasks", "duration", "budget")

        def create(self, validated_data):
            print("create management goal")
            tasks_data = validated_data.pop("tasks")
            management_goal = ManagementGoal.objects.create(**validated_data)
            TaskGoal.objects.create(management_goal=management_goal, **tasks_data)

    # https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    # https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects
