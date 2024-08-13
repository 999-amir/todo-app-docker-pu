from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from accounts.models import CostumeUser, ProfileModel
from django.shortcuts import get_object_or_404


@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = CostumeUser.objects.create_user(email='test@gmail.com', password='Aaa123!!')
    return user


@pytest.mark.django_db
class TestTodoAPI:
    def test_get_response_200(self, api_client, common_user):   # authenticated user get todo list
        url = reverse('todo:api_v1:todo-list')
        user = common_user
        api_client.force_authenticate(user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_get_response_401(self, api_client):    # unauthorized user get todo list
        url = reverse('todo:api_v1:todo-list')
        response = api_client.get(url)
        assert response.status_code == 401

    def test_post_response_201(self, api_client, common_user):  # authenticated user create new todo
        url = reverse('todo:api_v1:todo-list')
        user = common_user
        profile = get_object_or_404(ProfileModel, user=user)
        api_client.force_authenticate(user)
        data = {
            "profile": profile,
            "level": "green",
            "job": "Lorem Ipsum",
            "dead_end": "9999-09-09",
        }
        response = api_client.post(path=url, data=data)
        assert response.status_code == 201

    def test_post_response_400(self, api_client, common_user):  # unauthorized user create new todo
        url = reverse('todo:api_v1:todo-list')
        user = common_user
        profile = get_object_or_404(ProfileModel, user=user)
        api_client.force_authenticate(user)
        data = {
            "profile": profile,
            "level": "green",
        }
        response = api_client.post(path=url, data=data)
        assert response.status_code == 400
