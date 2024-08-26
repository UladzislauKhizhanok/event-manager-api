from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class UserTokenTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_obtain_token(self):
        url = reverse("token_obtain_pair")
        data = {
            "username": "testuser",
            "password": "password",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_obtain_token_invalid_credentials(self):
        url = reverse("token_obtain_pair")
        data = {
            "username": "testuser",
            "password": "wrongpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        url = reverse("token_obtain_pair")
        data = {
            "username": "testuser",
            "password": "password",
        }
        response = self.client.post(url, data, format="json")
        refresh_token = response.data["refresh"]

        url = reverse("token_refresh")
        data = {
            "refresh": refresh_token,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
