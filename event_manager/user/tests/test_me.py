from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class UserMeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)

    def test_get_current_user(self):
        url = reverse("me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_get_current_user_unauthenticated(self):
        self.client.logout()
        url = reverse("me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
