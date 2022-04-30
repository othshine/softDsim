from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers, status
from djongo.models import ObjectIdField


class TaskGoal(models.Model):
    """A `TaskGoal` is the part of a `ManagementGoal` of an `TemplateScenario`,
    that describes the number of tasks (of each Difficulty) that are the scope
    of an Template Scenario.

    :param easy: How many easy tasks?
    :type easy: int
    :param medium: How many medium tasks?
    :type medium: int
    :param hard: How many hard tasks?
    :type hard: int
    :param predecessor_p: Probability of a task having a predecessor
    :type predecessor_p: float [0 <= p <= 1]
    """

    id = ObjectIdField()
    easy = models.PositiveIntegerField()
    medium = models.PositiveIntegerField()
    hard = models.PositiveIntegerField()
    predecessor_p = models.FloatField(
        default=0.1,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )


class ManagementGoal(models.Model):
    """A `ManagementGoal` is the part of a `TemplateScenario` that describes
    what the goals, set by management, are. Including:

    duration: How many days are scheduled?
    budget: how many dollars can be spend?
    tasks: how many Tasks of which difficulty are part of the Scenario?

    :param models: _description_
    :type models: _type_
    """

    id = ObjectIdField()
    budget = models.FloatField()
    duration = models.PositiveSmallIntegerField()
    tasks = models.OneToOneField(TaskGoal, on_delete=models.CASCADE)


# Serializers


class TaskGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGoal
        fields = ("id", "easy", "medium", "hard", "predecessor_p")


class ManagementGoalSerializer(serializers.ModelSerializer):
    tasks = TaskGoalSerializer()

    class Meta:
        model = TaskGoal
        fields = ("id", "tasks", "duration", "budget")
