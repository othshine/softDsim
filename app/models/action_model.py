from djongo import models

from app.models.decision_models.answer_model import Answer


class Action(models.Model):

    id = models.ObjectIdField()
    title = models.TextField()
    typ = models.TextField()
    active = models.BooleanField()
    answer = models.ArrayField(Answer)
    required = models.BooleanField()
