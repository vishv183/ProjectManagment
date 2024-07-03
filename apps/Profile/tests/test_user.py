# tests/test_user_list_update.py
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User

from apps.Profile.models import CustomUser
from apps.Profile.tests.test_base import TestBase


class UserListUpdateViewTest(TestBase):

    def test_authenticated_user_list(self):
        response = self.user_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_superuser_list(self):
        response = self.superuser_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(len(response.data), 17)

    def test_unauthenticated_user_cannot_update_profile(self):
        updated_data = {
            'email': 'newuser@example.com',
            'mobile_number': '9876543210'
        }
        self.user_client.logout()
        response = self.client.patch(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        CustomUser = get_user_model()
        user = CustomUser.objects.get(pk=self.user.pk)
        self.assertNotEqual(user.email, 'newuser@example.com')
        self.assertNotEqual(user.mobile, '9876543210')

