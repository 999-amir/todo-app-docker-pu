from rest_framework.test import APIClient
from django.urls import reverse
import pytest


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.mark.django_db
class TestRegistration:

    def test_post_response_200(self, api_client):   # good request data
        url = reverse('accounts:api_v1:user:registration')
        data = {
            'email': 'test@gmail.com',
            'password': 'Aaa123##',
            'confirm_password': 'Aaa123##'
        }
        response = api_client.post(path=url, data=data)
        assert response.status_code == 200

    def test_post_response_400(self, api_client):   # bad request data
        url = reverse('accounts:api_v1:user:registration')
        data = {
            'email': 'test@gmail.com',
            'password': 'Aaa123##',
            'confirm_password': '99999999'
        }
        response = api_client.post(path=url, data=data)
        assert response.status_code == 400
