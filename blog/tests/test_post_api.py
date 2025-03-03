from http.client import responses
from datetime import datetime
import pytest
from rest_framework.test import APIClient
from django.urls import reverse,resolve
from accounts.models import User,Profile


@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def user_obj():
    user = User.objects.create_user(email="testuser@test.com", password="testpass")
    return user

@pytest.mark.django_db
class TestPostApi:
    def test_get_post_response_200_status(self,api_client,user_obj):
        url = reverse('blog:api-v1:post-list')
        user = user_obj
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_post_response_201_status(self,api_client,user_obj):
        url = reverse('blog:api-v1:post-list')

        data = {
            # 'author': self.profile_obj.id,
            'title' :'test-title',
            'content' : 'test-content' ,
            'status':True,
            'published_date':datetime.now()
        }
        user = user_obj
        api_client.force_authenticate(user=user)
        response = api_client.post(url,data)
        assert response.status_code == 201

    def test_post_response_403_status(self, api_client):
        url = reverse('blog:api-v1:post-list')
        data = {
            # 'author': self.profile_obj.id,
            'title': 'test-title',
            'content': 'test-content',
            'status': True,
            'published_date': datetime.now()
        }
        api_client.force_authenticate(user={})
        response = api_client.post(url, data)
        assert response.status_code == 403

    def test_post_response_in_valid_data(self, api_client, user_obj):
        url = reverse('blog:api-v1:post-list')

        data = {
            'status': True,
            'published_date': datetime.now()
        }
        user = user_obj
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400