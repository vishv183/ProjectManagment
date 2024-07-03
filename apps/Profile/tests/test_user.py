# tests/test_user_list_update.py
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User

from apps.Profile.models import CustomUser
from apps.Profile.tests.test_base import TestBase


class UserListUpdateViewTest(TestBase):

    def setUp(self):
        super().setUp()
        self.url = '/api-profile/users/'

    def test_authenticated_user_list(self):
        response = self.user_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # print(response.data)

    def test_unauthenticated_user_list(self):
        self.user_client.logout()
        response = self.user_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_superuser_list(self):
        response = self.superuser_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

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

    def test_authenticated_user_can_update_own_profile(self):
        updated_data = {
            "email": "newemail@example.com",
            "mobile": "6355447669",
        }
        response = self.user_client.patch(f'/api-profile/users/{self.user.id}/', updated_data, format='json')
        # print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['mobile'], updated_data['mobile'])

    def test_authenticated_superuser_can_update_all_profile(self):
        updated_data = {
            "email": "newemail@example.com",
            "mobile": "1355447669",
        }
        response = self.superuser_client.patch(f'/api-profile/users/{self.user.id}/', updated_data, format='json')
        # print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['mobile'], updated_data['mobile'])

    def test_unauthenticated_superuser_cannot_update_all_profile(self):
        updated_data = {
            "email": "superuser@example.com",
            "mobile": "1355447669",
        }
        response = self.user_client.patch(f'/api-profile/users/{self.user.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_unauthenticated_superuser_cannot_update_all_profile(self):
        updated_data = {
            "email": "superuser@example.com",
            "mobile": "1355447669",
        }
        self.user_client.logout()
        response = self.user_client.patch(f'/api-profile/users/{self.user.id}/', updated_data, format='json')

        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_delete_own_profile(self):
        self.user_client.force_authenticate(user=self.user)
        response = self.user_client.delete(f'/api-profile/users/{self.user.id}/')
        if response.status_code == status.HTTP_204_NO_CONTENT:
            print("Profile deleted successfully")
        else:
            print(response.content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(pk=self.user.id).exists())

    def test_authenticated_superuser_can_delete_other_profile(self):
        another_user = CustomUser.objects.create_user(
            email='anotheruser@example.com', password='anotherpassword'
        )
        self.superuser_client.force_authenticate(user=self.superuser)
        url = f'/api-profile/users/{another_user.id}/'
        response = self.superuser_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(pk=another_user.pk).exists())

    def test_unauthenticated_user_cannot_delete_profile(self):
        self.user_client.logout()
        response = self.user_client.delete(f'/api-profile/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(CustomUser.objects.filter(pk=self.user.pk).exists())
