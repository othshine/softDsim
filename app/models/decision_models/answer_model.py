from djongo import models


class Answer(models.Model):
    id = models.ObjectIdField()
    test = models.TextField()
