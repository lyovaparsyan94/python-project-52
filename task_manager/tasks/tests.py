from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='user',
            password='password'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password'
        )
        self.client.login(
            username='user',
            password='password'
        )
        self.label = Label.objects.create(name='label')
        self.label2 = Label.objects.create(name='label2')
        self.label3 = Label.objects.create(name='label3')

        self.status = Status.objects.create(name='status')
        self.status2 = Status.objects.create(name='status2')
        self.task = Task.objects.create(
            name='taskop',
            creator=self.user,
            status=self.status,
            executor=self.user,
        )
        self.task.labels.add(self.label, self.label2)

        self.task2 = Task.objects.create(
            name='taskipo',
            creator=self.user2,
            status=self.status2,
            executor=self.user2,
        )
        self.task2.labels.add(self.label3)

        self.task3 = Task.objects.create(
            name='task3',
            creator=self.user,
            status=self.status2,
            executor=self.user2,
        )
        self.task3.labels.add(self.label2, self.label3)

    def test_update_task(self):
        data = {
            "name": "taskno1",
            "description": "description",
            "status": self.status.id,
        }

        response = self.client.post(
            reverse('task_update', args=[self.task.id]), data
        )

        self.assertEqual(response.status_code, 302)

        new_task = Task.objects.get(pk=self.task.id)
        self.assertEqual(new_task.name, data['name'])
        self.assertEqual(new_task.description, data['description'])
        
    def test_task_delete(self):
        response = self.client.post(
            reverse('task_delete', args=[self.task3.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)
        
        response = self.client.post(
            reverse('task_delete', args=[self.task2.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)
        
    def test_filter_task_my_tasks(self):
        data = {
            'own_task': 'on'
        }
        response = self.client.get(reverse('all_tasks'), data)
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task3.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_task_labels(self):
        data = {
            'labels': self.label.id
        }
        response = self.client.get(reverse('all_tasks'), data)
        self.assertContains(response, self.task.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)

    def test_filter_task_statuses(self):
        data = {
            'status': self.status.id
        }
        response = self.client.get(reverse('all_tasks'), data)
        self.assertContains(response, self.task.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)

    def test_filter_task_executor(self):
        data = {
            'executor': self.user2.id
        }
        response = self.client.get(reverse('all_tasks'), data)
        self.assertContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)
        self.assertNotContains(response, self.task.name)

