from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from accounts.models import CostumeUser
from rest_framework_simplejwt.tokens import RefreshToken


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
class TestActivation:

    def test_get_response_200(self, api_client):  # token is correct (user verified successfully)
        user = common_user()
        token = get_token_for_user(user['user'])
        url = reverse('accounts:api_v1:user:activation', kwargs={'token': token})
        response = api_client.get(path=url)
        assert response.status_code == 200
        assert CostumeUser.objects.get(id=user['user'].id).is_verify is True

    def test_get_response_400(self, api_client):  # token is incorrect (user verified failed)
        user = common_user()
        url = reverse('accounts:api_v1:user:activation', kwargs={'token': '123456789'})
        response = api_client.get(path=url)
        assert response.status_code == 400
        assert CostumeUser.objects.get(id=user['user'].id).is_verify is False


@pytest.mark.django_db
class TestActivationResend:

    def test_post_response_200(self, api_client):    # token resend successfully for available user in db
        user = common_user()
        data = {
            'email': user['user'].email
        }
        url = reverse('accounts:api_v1:user:activation-resend')
        response = api_client.post(path=url, data=data)
        assert response.status_code == 200

    def test_post_response_404(self, api_client):    # token resend failed ( unavailable user in db )
        data = {
            'email': 'unavailable@user.com'
        }
        url = reverse('accounts:api_v1:user:activation-resend')
        response = api_client.post(path=url, data=data)
        assert response.status_code == 404