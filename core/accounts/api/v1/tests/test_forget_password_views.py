from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
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


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@pytest.mark.django_db
class TestForgetPassword:

    def test_post_response_200(self, api_client):  # token send successfully for available user in db
        user = common_user()
        data = {
            'email': user['user'].email
        }
        url = reverse('accounts:api_v1:user:forget-password')
        response = api_client.post(path=url, data=data)
        assert response.status_code == 200

    def test_post_response_404(self, api_client):  # token send failed ( unavailable user in db )
        data = {
            'email': 'unavailable@user.com'
        }
        url = reverse('accounts:api_v1:user:forget-password')
        response = api_client.post(path=url, data=data)
        assert response.status_code == 404


@pytest.mark.django_db
class TestForgetPasswordConfirm:
    def test_post_response_200(self, api_client):  # password changed successfully
        user = common_user()
        token = get_token_for_user(user['user'])
        data = {
            'pass1': 'Bbb234!!',
            'pass2': 'Bbb234!!',
        }
        url = reverse('accounts:api_v1:user:confirm-forget-password', kwargs={'token': token})
        response = api_client.post(path=url, data=data)
        assert response.status_code == 200

    def test_post_response_400_token(self, api_client):  # token is incorrect ( password not change )
        user = common_user()
        token = get_token_for_user(user['user'])
        data = {
            'pass1': 'Bbb234!!',
            'pass2': 'Bbb234!!',
        }
        url = reverse('accounts:api_v1:user:confirm-forget-password', kwargs={'token': '123456789'})
        response = api_client.post(path=url, data=data)
        assert response.status_code == 400

    def test_post_response_400_password(self, api_client):  # password is incorrect (password not change)
        user = common_user()
        token = get_token_for_user(user['user'])
        data = {
            'pass1': 'Bbb234!!',
            'pass2': 'Aaa123##',
        }
        url = reverse('accounts:api_v1:user:confirm-forget-password', kwargs={'token': token})
        response = api_client.post(path=url, data=data)
        assert response.status_code == 400
