from django.test import Client, TestCase

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class LabelTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass'
        )
        self.label = Label.objects.create(
            name='Test Label', 
            creator=self.user
        )
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            creator=self.user
        )
        self.label_data = {'name': 'New Label'}
