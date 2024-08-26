from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class UserRegisterTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        url = reverse("register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "password123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], data["username"])
        self.assertIn("tokens", response.data)

    def test_register_user_invalid_data(self):
        url = reverse("register")
        data = {
            "username": "",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "password123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
