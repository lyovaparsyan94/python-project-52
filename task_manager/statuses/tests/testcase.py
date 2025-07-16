from django.test import Client, TestCase

from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass'
        )
        self.status = Status.objects.create(name='Test Status')
        self.status_data = {'name': 'New Status'}
