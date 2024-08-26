from django.urls import reverse
from event.tests.base_test_case import BaseTestCase
from rest_framework import status


class EventDeleteTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.event = self.create_event(self.user)

    def test_delete_event(self):
        url = reverse("event-detail", args=[self.event.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_event_unauthenticated(self):
        self.client.logout()

        response = self.client.delete(reverse("event-detail", args=[self.event.id]))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_event_forbidden(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(reverse("event-detail", args=[self.event.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
