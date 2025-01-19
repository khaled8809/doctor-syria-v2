import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_password():
    return "test-pass123"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = "testuser"
        if "email" not in kwargs:
            kwargs["email"] = "test@example.com"
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, api_client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        api_client.login(username=user.username, password=test_password)
        return api_client, user

    return make_auto_login
