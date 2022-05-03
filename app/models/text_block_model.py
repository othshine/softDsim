from djongo import models


class TextBlock(models.Model):
    id = models.ObjectIdField()
    title = models.TextField()
