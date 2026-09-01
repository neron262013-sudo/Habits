from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def test_create_user(self):
        """Тестирование регистрации пользователя"""
        data = {
            "email": "new@example.com",
            "password": "testpassword",
        }

        response = self.client.post("/users/register/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(User.objects.filter(email="new@example.com").exists())

    def test_login_user(self):
        """Тестирование авторизации пользователя"""
        user = User(email="login@example.com")
        user.set_password("testpassword")
        user.save()

        response = self.client.post(
            "/users/login/",
            data={
                "email": "login@example.com",
                "password": "testpassword",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("access", response.json())

        self.assertIn("refresh", response.json())

    def test_refresh_token(self):
        """Тестирование обновления токена"""
        user = User(email="refresh@example.com")
        user.set_password("testpassword")
        user.save()

        response = self.client.post(
            "/users/login/",
            data={
                "email": "refresh@example.com",
                "password": "testpassword",
            },
        )

        refresh_token = response.json()["refresh"]

        response = self.client.post(
            "/users/token/refresh/",
            data={
                "refresh": refresh_token,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("access", response.json())
