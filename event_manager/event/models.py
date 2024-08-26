from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class EventTypeEnum(models.TextChoices):
    CONFERENCE = "conference", "Conference"
    WORKSHOP = "workshop", "Workshop"
    MEETUP = "meetup", "Meetup"
    WEBINAR = "webinar", "Webinar"


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    capacity = models.IntegerField()
    type = models.CharField(max_length=50, choices=EventTypeEnum.choices, default=EventTypeEnum.CONFERENCE)
    attendees = models.ManyToManyField(User, related_name="events_attending", blank=True)
    created_by = models.ForeignKey(User, related_name="events_created", on_delete=models.CASCADE)

    def is_past_event(self):
        return self.end_date < timezone.now()

    def __str__(self):
        return f"{self.id} | {self.name}"
