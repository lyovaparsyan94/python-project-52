import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages

User = get_user_model()


@pytest.mark.django_db
class TestUsers:
    
    def test_create_user(self, client):
        data = {
            'username': 'testuser',
            'password1': '12345test',
            'password2': '12345test',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = client.post(reverse('users:create_user'), data, follow=True)
        
        assert response.status_code == 200
        assert User.objects.filter(username='testuser').exists()
    
    def test_user_list(self, client):
        User.objects.create_user(username='testuser', password='12345test')
        response = client.get(reverse('users:users'))
        
        assert response.status_code == 200
        assert 'testuser' in response.content.decode() 