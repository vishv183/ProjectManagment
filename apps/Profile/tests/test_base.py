from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

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
        self.refresh = RefreshToken.for_user(self.user)
        self.access = str(self.refresh.access_token)

        self.user_client = APIClient()
        self.user_client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        # self.user_client.force_authenticate(user=self.user)

        self.superuser_refresh = RefreshToken.for_user(self.superuser)
        self.superuser_access = str(self.superuser_refresh.access_token)

        self.superuser_client = APIClient()
        self.superuser_client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.superuser_access}")
        self.superuser_client.force_authenticate(user=self.superuser)

        super().setUp()