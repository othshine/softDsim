from django.db import models


class Simulation(models.Model):
    id = models.AutoField(primary_key=True)
    # text = models.ArrayField(TextBlock)
    continue_text = models.TextField()
    points = models.PositiveIntegerField()
    # actions = models.ArrayField(Action)
    # score_card = models.OneToOneField(ScoreCard, on_delete=models.CASCADE)
