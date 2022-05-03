from djongo import models


class ScoreCard(models.Model):
    id = models.ObjectIdField()
    easy = models.PositiveIntegerField()
    medium = models.PositiveIntegerField()
    hard = models.PositiveIntegerField()
