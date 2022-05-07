from django.db import models

from app.models.decision_models.decision_model import Decision


class Action(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.TextField()
    typ = models.TextField()
    active = models.BooleanField()
    # answers: List[Answer] -> ForeignKey Reference in Answer Model
    required = models.BooleanField()

    decision = models.ForeignKey(
        Decision,
        on_delete=models.CASCADE,
        related_name="actions",
        blank=True,
        null=True,
    )
