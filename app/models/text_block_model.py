from django.db import models

from app.models.decision_models.decision_model import Decision
from app.models.simulation_models.simulation_model import Simulation


class TextBlock(models.Model):
    """
    A `TextBlock` contains a header and content of a Text displayed to the user
    header: header of content
    content: text content
    decision: foreign key to decision
    simulation: foreign key to simulation
    """

    id = models.AutoField(primary_key=True)
    header = models.TextField()
    content = models.TextField()

    decision = models.ForeignKey(
        Decision,
        on_delete=models.CASCADE,
        related_name="text_block",
        blank=True,
        null=True,
    )

    simulation = models.ForeignKey(
        Simulation,
        on_delete=models.CASCADE,
        related_name="text_block",
        blank=True,
        null=True,
    )
