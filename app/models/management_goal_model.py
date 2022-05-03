from djongo import models
from django.core.validators import MaxValueValidator, MinValueValidator


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

    id = models.ObjectIdField()
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
    budget: how many dollars can be spent?
    tasks: how many Tasks of which difficulty are part of the Scenario?
    :param models: _description_
    :type models: _type_
    """

    id = models.ObjectIdField()
    budget = models.FloatField()
    duration = models.PositiveSmallIntegerField()
    tasks = models.OneToOneField(
        TaskGoal,
        on_delete=models.CASCADE,
    )


# tasks = models.EmbeddedField(model_container=TaskGoal)

# objects = models.DjongoManager()


# from django.core.validators import MinValueValidator, MaxValueValidator
# from django_mongoengine import Document, EmbeddedDocument, fields
#
#
# class TaskGoal(EmbeddedDocument):
#
#     id = fields.ObjectIdField()
#     easy = fields.DecimalField()
#     medium = fields.DecimalField()
#     hard = fields.DecimalField()
#     predecessor_p = fields.FloatField(
#         default=0.1,
#         validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
#     )
#
#
# class ManagementGoal(Document):
#
#     id = fields.ObjectIdField()
#     budget = fields.FloatField()
#     duration = fields.DecimalField()
#     tasks = fields.EmbeddedDocumentField("TaskGoal")
