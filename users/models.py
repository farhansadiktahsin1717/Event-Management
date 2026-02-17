from django.db import models


class Participant(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    events = models.ManyToManyField("events.Event", related_name="participants")

    def __str__(self):
        return self.name
