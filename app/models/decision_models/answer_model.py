from django.db import models

from app.models.action_model import Action


class Answer(models.Model):

    id = models.AutoField(primary_key=True)
    label = models.TextField()
    points = models.PositiveIntegerField()

    action = models.ForeignKey(
        Action,
        on_delete=models.CASCADE,
        related_name="answer",
        blank=True,
        null=True,
    )
