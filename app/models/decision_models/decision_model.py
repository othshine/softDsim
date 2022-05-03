from djongo import models

from app.models.action_model import Action
from app.models.text_block_model import TextBlock


class Decision(models.Model):
    id = models.ObjectIdField()
    text = models.ArrayField(TextBlock)
    continue_text = models.TextField()
    points = models.PositiveIntegerField()
    actions = models.ArrayField(Action)
