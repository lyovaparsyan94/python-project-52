import types

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from task_manager.rollbar_middleware import CustomRollbarNotifierMiddleware


def dummy_get_response(request):
    return None


@pytest.mark.django_db
def test_index_view(client):
    url = reverse("index")
    response = client.get(url)

    assert response.status_code == 200
    templates = [t.name for t in response.templates if t.name]
    assert "index.html" in templates


def test_get_extra_data():
    middleware = CustomRollbarNotifierMiddleware(dummy_get_response)
    request = types.SimpleNamespace()
    exc = Exception()

    data = middleware.get_extra_data(request, exc)
    assert 'feature_flags' in data
    assert data['feature_flags'] == ['feature_1', 'feature_2']


@pytest.mark.django_db
def test_get_payload_data_authenticated_user(db):
    User = get_user_model()
    
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='pass',
        first_name='Test',
        last_name='User'
    )
    request = types.SimpleNamespace()
    request.user = user
    exc = Exception()

    middleware = CustomRollbarNotifierMiddleware(dummy_get_response)
    payload = middleware.get_payload_data(request, exc)

    assert 'person' in payload
    assert payload['person']['username'] == 'testuser'
    assert payload['person']['email'] == 'test@example.com'


def test_get_payload_data_anonymous_user():
    request = types.SimpleNamespace()
    request.user = AnonymousUser()
    exc = Exception()

    middleware = CustomRollbarNotifierMiddleware(dummy_get_response)
    payload = middleware.get_payload_data(request, exc)
    assert payload == {}