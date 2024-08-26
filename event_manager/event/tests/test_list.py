from django.urls import reverse
from event.models import EventTypeEnum
from event.tests.base_test_case import BaseTestCase
from rest_framework import status


class EventTests(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.event1 = self.create_event(self.user)
        self.event2 = self.create_event(self.user, name="Event 2", future=True, event_type=EventTypeEnum.WORKSHOP)

    def test_list_events(self):
        response = self.client.get(reverse("event-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_list_events_with_filters(self):
        url = reverse("event-list")

        response = self.client.get(url, {"type": EventTypeEnum.CONFERENCE})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Event 1")

        response = self.client.get(url, {"type": EventTypeEnum.WORKSHOP})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Event 2")

        response = self.client.get(url, {"start_date": "2024-08-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_list_events_unauthenticated(self):
        self.client.logout()

        response = self.client.get(reverse("event-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
