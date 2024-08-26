from django.urls import reverse
from event.models import EventTypeEnum
from event.tests.base_test_case import BaseTestCase
from rest_framework import status


class EventCreateTests(BaseTestCase):
    def test_create_event(self):
        url = reverse("event-list")

        data = {
            "name": "New Event",
            "description": "Test description",
            "start_date": "2024-08-01T10:00:00Z",
            "end_date": "2024-08-01T12:00:00Z",
            "capacity": 100,
            "type": EventTypeEnum.CONFERENCE,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["description"], data["description"])

    def test_create_event_unauthenticated(self):
        self.client.logout()

        url = reverse("event-list")

        data = {
            "name": "New Event",
            "description": "Test description",
            "start_date": "2024-08-01T10:00:00Z",
            "end_date": "2024-08-01T12:00:00Z",
            "capacity": 100,
            "type": EventTypeEnum.CONFERENCE,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_event_invalid_data(self):
        url = reverse("event-list")

        data = {
            "name": "",
            "description": "Test description",
            "start_date": "2024-08-01T10:00:00Z",
            "end_date": "2024-08-01T12:00:00Z",
            "capacity": 100,
            "type": EventTypeEnum.CONFERENCE,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
