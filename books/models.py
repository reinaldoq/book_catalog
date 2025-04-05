import uuid

from django.db import models
from model_utils.models import TimeStampedModel


class Book(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title
