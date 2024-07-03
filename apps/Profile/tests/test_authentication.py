from rest_framework import status
from .test_base import TestBase


class TestAuth(TestBase):
    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_custom_token_obtain_pair(self):
        print("function 2 is working")

        registration_response = self.client.post(self.register_url, self.user_data, format='json')
        print(f"Registration response status: {registration_response.status_code}")
        print(f"Registration response content: {registration_response.content}")
        self.assertEqual(registration_response.status_code,
                         status.HTTP_201_CREATED)

        token_response = self.client.post(self.token_obtain_url, self.user_data, format='json')
        print(f"Token response status: {token_response.status_code}")
        print(f"Token response content: {token_response.content}")
        response = token_response.json()

        self.assertIn('access', response)
        self.assertIn('refresh', response)
