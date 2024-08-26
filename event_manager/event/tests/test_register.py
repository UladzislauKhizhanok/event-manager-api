from django.urls import reverse
from event.tests.base_test_case import BaseTestCase
from rest_framework import status


class EventRegisterTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.event = self.create_event(self.user, future=True)

    def test_register_event(self):
        response = self.client.post(reverse("event-register", args=[self.event.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Successfully registered for the event.")
        self.assertIn(self.user, self.event.attendees.all())

    def test_register_event_not_found(self):
        response = self.client.post(reverse("event-register", args=[-1]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_register_multiple_users(self):
        url = reverse("event-register", args=[self.event.id])

        # Register first user
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Successfully registered for the event.")
        self.assertIn(self.user, self.event.attendees.all())

        # Register second user
        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Successfully registered for the event.")
        self.assertIn(self.other_user, self.event.attendees.all())

    def test_register_past_event(self):
        past_event = self.create_event(self.user, future=False)

        url = reverse("event-register", args=[past_event.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Cannot register for past events.")

    def test_register_event_capacity_reached(self):
        capacity_event = self.create_event(self.user, future=True, capacity=1)

        url = reverse("event-register", args=[capacity_event.id])

        # Register first user
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Successfully registered for the event.")
        self.assertIn(self.user, capacity_event.attendees.all())

        # Register second user
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Event capacity reached.")
