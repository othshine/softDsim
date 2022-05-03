from djongo import models

from app.models.action_model import Action
from app.models.simulation_models.score_card_model import ScoreCard
from app.models.text_block_model import TextBlock


class Simulation(models.Model):
    id = models.ObjectIdField()
    text = models.ArrayField(TextBlock)
    continue_text = models.TextField()
    points = models.PositiveIntegerField()
    actions = models.ArrayField(Action)
    score_card = models.OneToOneField(ScoreCard, on_delete=models.CASCADE)
