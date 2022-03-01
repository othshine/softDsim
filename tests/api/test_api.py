from rest_framework.test import APIClient
import pytest
from django.contrib.auth.models import User


PASSWORD = 'supersecret'

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def user():
    user = User.objects.create_user(username='peterson',
                                 email='peterson@frauas.de',
                                 password=PASSWORD)
    return user

@pytest.mark.django_db
def test_index_redirect_to_login(api_client: APIClient, user):
    response = api_client.get('/')
    assert response.status_code == 302

@pytest.mark.django_db
def test_index_when_logged_in(api_client: APIClient, user):
    api_client.login(username=user.username, password=PASSWORD)
    response = api_client.get('/')
    assert response.status_code == 200



