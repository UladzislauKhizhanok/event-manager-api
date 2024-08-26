from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from event.models import Event, EventTypeEnum
from rest_framework.test import APIClient


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user("testuser", "password")
        self.other_user = self.create_user("otheruser", "password")
        self.client.force_authenticate(user=self.user)

    def create_user(self, username, password):
        return User.objects.create_user(username=username, password=password)

    def create_event(
        self,
        user,
        future=True,
        capacity=100,
        event_type=EventTypeEnum.CONFERENCE,
        name="Event 1",
    ):
        start_date = timezone.now() + timedelta(days=1) if future else timezone.now() - timedelta(days=2)

        end_date = start_date + timedelta(hours=2)

        return Event.objects.create(
            name=name,
            description="Test description",
            start_date=start_date,
            end_date=end_date,
            capacity=capacity,
            type=event_type,
            created_by=user,
        )
