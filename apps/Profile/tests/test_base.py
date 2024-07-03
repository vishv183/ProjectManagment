from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.Profile.models import CustomUser

SUPERUSER_EMAIL = ''


class TestBase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        CustomUser = get_user_model()
        self.superuser = CustomUser.objects.create_superuser(
            email='superuser@example.com', password='superpassword'
        )
        self.user = CustomUser.objects.create_user(
            email='user@example.com', password='userpassword'
        )
        self.user_client = APIClient()
        self.user_client.login(email="user@example.com", password="userpassword")

        self.superuser_client = APIClient()
        self.superuser_client.login(email='superuser@example.com', password='superpassword')
        self.url = f'/api-profile/users/{self.user.pk}/'

        super().setUp()