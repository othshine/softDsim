from django.db import models


class ScoreCard(models.Model):
    id = models.AutoField(primary_key=True)
    easy = models.PositiveIntegerField()
    medium = models.PositiveIntegerField()
    hard = models.PositiveIntegerField()
