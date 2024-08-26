from django.urls import reverse
from event.tests.base_test_case import BaseTestCase
from rest_framework import status


class EventGetTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.event = self.create_event(self.user)

    def test_get_event_by_id(self):
        response = self.client.get(reverse("event-detail", args=[self.event.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.event.name)

    def test_get_event_by_id_not_found(self):
        response = self.client.get(reverse("event-detail", args=[-1]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_event_by_id_unauthenticated(self):
        self.client.logout()

        response = self.client.get(reverse("event-detail", args=[self.event.id]))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
