from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from accounts.models import CostumeUser, ProfileModel
from todo.models import TodoModel
from django.shortcuts import get_object_or_404
from datetime import datetime


@pytest.fixture
def api_client():
    client = APIClient()
    return client


def common_user_profile_task():
    user = CostumeUser.objects.create_user(email='test@gmail.com', password='Aaa123!!')
    profile = get_object_or_404(ProfileModel, user=user)    # profile will auto generate with signal
    task = TodoModel.objects.create(level='green', profile=profile, job='lorem ipsum', dead_end=datetime.now())
    return {
        'user': user,
        'profile': profile,
        'task': task
    }


@pytest.mark.django_db
class TestTodoDetailAPI:

    def test_get_response_401(self, api_client):  # unauthorized user get todo task
        data = common_user_profile_task()
        url = reverse('todo:api_v1:todo-detail', kwargs={'pk': data['task'].pk})
        response = api_client.get(url)
        assert response.status_code == 401

    def test_get_response_200(self, api_client):  # authenticated user get todo task
        data = common_user_profile_task()
        url = reverse('todo:api_v1:todo-detail', kwargs={'pk': data['task'].pk})
        api_client.force_authenticate(data['user'])
        response = api_client.get(url)
        assert response.status_code == 200

    def test_put_response_200(self, api_client):  # authenticated user update todo task
        data = common_user_profile_task()
        url = reverse('todo:api_v1:todo-detail', kwargs={'pk': data['task'].pk})
        api_client.force_authenticate(data['user'])
        update_task_data = {
            "profile": data['profile'],
            "level": "green",
            "job": "Lorem Ipsum",
            "dead_end": "9999-09-09",
        }
        response = api_client.put(path=url, data=update_task_data)
        assert response.status_code == 200

    def test_delete_response_200(self, api_client):  # authenticated user delete todo task
        data = common_user_profile_task()
        url = reverse('todo:api_v1:todo-detail', kwargs={'pk': data['task'].pk})
        api_client.force_authenticate(data['user'])
        response = api_client.delete(path=url)
        assert response.status_code == 204
