from django.db import models

from app.models.simulation_fragment import SimulationFragment


class Action(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.TextField()
    typ = models.TextField()
    lower_limit = models.IntegerField()
    upper_limit = models.IntegerField()

    simulation_fragment = models.ForeignKey(
        SimulationFragment,
        on_delete=models.CASCADE,
        related_name="actions",
        blank=True,
        null=True,
    )
