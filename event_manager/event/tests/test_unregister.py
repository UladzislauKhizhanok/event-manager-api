from django.urls import reverse
from event.tests.base_test_case import BaseTestCase
from rest_framework import status


class EventUnregisterTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.event = self.create_event(self.user, future=True)
        self.event.attendees.add(self.user)
        self.event.attendees.add(self.other_user)

    def test_unregister_event(self):
        response = self.client.post(reverse("event-unregister", args=[self.event.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Successfully unregistered from the event.")
        self.assertNotIn(self.user, self.event.attendees.all())

    def test_unregister_event_not_found(self):
        response = self.client.post(reverse("event-unregister", args=[-1]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unregister_event_unauthenticated(self):
        self.client.logout()

        response = self.client.post(reverse("event-unregister", args=[self.event.id]))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unregister_past_event(self):
        past_event = self.create_event(self.user, future=False)
        past_event.attendees.add(self.user)

        response = self.client.post(reverse("event-unregister", args=[past_event.id]))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Cannot unregister from past events.")

    def test_unregister_multiple_users(self):
        url = reverse("event-unregister", args=[self.event.id])

        # Unregister first user
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Successfully unregistered from the event.")
        self.assertNotIn(self.user, self.event.attendees.all())

        # Unregister second user
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Successfully unregistered from the event.")
        self.assertNotIn(self.other_user, self.event.attendees.all())
