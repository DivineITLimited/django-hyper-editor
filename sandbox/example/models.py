from django.db import models
from hypereditor.fields import HyperField


class Page(models.Model):
    title = models.CharField(max_length=255)
    content = HyperField(default=None)

    def __str__(self):
        return self.title