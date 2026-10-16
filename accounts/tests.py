from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class AuthTests(APITestCase):
    def test_register_patient(self):
        response = self.client.post("/api/auth/register/", {
            "full_name": "Test Patient",
            "email": "test@example.com",
            "password": "StrongPassword123!",
            "role": "patient",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_login(self):
        User.objects.create_user(
            email="login@example.com",
            password="StrongPassword123!",
            full_name="Login User",
            role="patient"
        )
        response = self.client.post("/api/auth/login/", {
            "email": "login@example.com",
            "password": "StrongPassword123!"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
