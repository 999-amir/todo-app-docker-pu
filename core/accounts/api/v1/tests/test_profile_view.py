from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from accounts.models import CostumeUser


@pytest.fixture
def api_client():
    client = APIClient()
    return client


def common_user():
    return {
        'user': CostumeUser.objects.create_user(email='test@gmail.com', password='Aaa123##'),
    }


@pytest.mark.django_db
class TestRegistration:

    def test_get_response_200(self, api_client):   # get profile for authenticated user
        user = common_user()['user']
        url = reverse('accounts:api_v1:profile:profile')
        api_client.force_authenticate(user)
        response = api_client.get(path=url)
        assert response.status_code == 200

    def test_get_response_401(self, api_client):   # unauthenticated user
        url = reverse('accounts:api_v1:profile:profile')
        response = api_client.get(path=url)
        assert response.status_code == 401

