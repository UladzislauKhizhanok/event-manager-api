from django.urls import reverse
from event.tests.base_test_case import BaseTestCase
from rest_framework import status


class EventPartialUpdateTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.event = self.create_event(self.user)

    def test_partial_update_event(self):
        data = {
            "name": "Partially Updated Event",
        }

        response = self.client.patch(reverse("event-detail", args=[self.event.id]), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])

    def test_partial_update_event_unauthenticated(self):
        self.client.logout()

        data = {
            "name": "Partially Updated Event",
        }

        response = self.client.patch(reverse("event-detail", args=[self.event.id]), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_event_forbidden(self):
        self.client.force_authenticate(user=self.other_user)

        data = {
            "name": "Partially Updated Event",
        }

        response = self.client.patch(reverse("event-detail", args=[self.event.id]), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
