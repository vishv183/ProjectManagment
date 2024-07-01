from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


# Create your tests here.

class TestAuthViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.token_url = reverse('custom-token-obtain-pair')
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
        }

        def test_register_user(self):
            print("function 1 is working ")
            response = self.client.post(self.register_url, self.user_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_token_obtain_pair(self):
            print("function2 is working ")
            self.client.post(self.register_url, self.user_data, format='json')

            response = self.client.post(self.token_url, self.user_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('access', response.data)
            self.assertIn('refresh', response.data)