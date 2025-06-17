import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from task_manager.tasks.models import Task, Status

User = get_user_model()


@pytest.mark.django_db
class TestTasks:
    
    def test_task_list_requires_login(self, client):
        response = client.get(reverse('tasks:task_list'))
        assert response.status_code == 302
    
    def test_task_list_with_login(self, client):
        user = User.objects.create_user(username='testuser', password='12345test')
        client.login(username='testuser', password='12345test')
        
        response = client.get(reverse('tasks:task_list'))
        assert response.status_code == 200 