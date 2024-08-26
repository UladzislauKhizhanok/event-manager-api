from django.urls import reverse
from event.models import EventTypeEnum
from event.tests.base_test_case import BaseTestCase
from rest_framework import status


class EventUpdateTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.event = self.create_event(self.user)

    def test_update_event(self):
        url = reverse("event-detail", args=[self.event.id])

        data = {
            "name": "Updated Event",
            "description": "Updated description",
            "start_date": "2024-08-01T10:00:00Z",
            "end_date": "2024-08-01T12:00:00Z",
            "capacity": 150,
            "type": EventTypeEnum.WORKSHOP,
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["description"], data["description"])

    def test_update_event_unauthenticated(self):
        self.client.logout()

        url = reverse("event-detail", args=[self.event.id])

        data = {
            "name": "Updated Event",
            "description": "Updated description",
            "start_date": "2024-08-01T10:00:00Z",
            "end_date": "2024-08-01T12:00:00Z",
            "capacity": 150,
            "type": EventTypeEnum.WORKSHOP,
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_event_forbidden(self):
        self.client.force_authenticate(user=self.other_user)

        url = reverse("event-detail", args=[self.event.id])

        data = {
            "name": "Updated Event",
            "description": "Updated description",
            "start_date": "2024-08-01T10:00:00Z",
            "end_date": "2024-08-01T12:00:00Z",
            "capacity": 150,
            "type": EventTypeEnum.WORKSHOP,
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
