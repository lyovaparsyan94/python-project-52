from django.test import Client, TestCase

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass'
        )
        
        self.status1 = Status.objects.create(name='Status1')
        self.status2 = Status.objects.create(name='Status2')
        
        self.label1 = Label.objects.create(
            name='Label1', 
            creator=self.user
        )
        self.label2 = Label.objects.create(
            name='Label2', 
            creator=self.user
        )
        
        self.task1 = Task.objects.create(
            name='Task with Status1',
            status=self.status1,
            creator=self.user,
            executor=self.user
        )
        self.task1.labels.add(self.label1)
        
        self.task2 = Task.objects.create(
            name='Task with Status2',
            status=self.status2,
            creator=self.user,
            executor=self.other_user
        )
        self.task2.labels.add(self.label2)
        
        self.task3 = Task.objects.create(
            name='Other user task',
            status=self.status1,
            creator=self.other_user,
            executor=self.user
        )
        
        self.client.login(username='testuser', password='testpass')
        
        self.task_data = {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status1.pk,
        }
