from django.conf import settings
from django.urls import reverse

from task_manager.tasks.models import Task

from .testcase import TaskTestCase


class TaskViewsTest(TaskTestCase):
    def test_task_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks_list'))
        self.assertRedirects(
            response,
            f'/{settings.LANGUAGE_CODE}/login/?next=/{settings.LANGUAGE_CODE}/tasks/'
        )

    def test_task_create(self):
        response = self.client.post(
            reverse('task_create'),
            self.task_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update(self):
        response = self.client.post(
            reverse('task_update', args=[self.task1.pk]),
            {
                'name': 'Updated Task',
                'description': 'Updated Description',
                'status': self.status1.pk,
                'executor': self.user.pk,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, 'Updated Task')

    def test_task_delete(self):
        response = self.client.post(
            reverse('task_delete', args=[self.task1.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    def test_task_delete_only_by_creator(self):
        self.client.logout()
        self.client.login(username='otheruser', password='testpass')
        response = self.client.post(
            reverse('task_delete', args=[self.task1.pk])
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())
