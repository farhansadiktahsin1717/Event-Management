from django.conf import settings
from django.db import models

from categories.models import Category


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    image = models.ImageField(upload_to="events/", default="events/default_event.jpg")
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="rsvp_events",
        blank=True,
    )

    def __str__(self):
        return self.name
