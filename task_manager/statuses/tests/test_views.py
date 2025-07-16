from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

from .testcase import StatusTestCase


class StatusViewsTest(StatusTestCase):
    def test_status_list_requires_login(self):
        response = self.client.get(reverse('statuses_list'))
        self.assertRedirects(
            response,
            f'/{settings.LANGUAGE_CODE}/login/?next=/{settings.LANGUAGE_CODE}/statuses/'
        )

    def test_status_create(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('status_create'),
            self.status_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('status_update', args=[self.status.pk]),
            {'name': 'Updated Status'}
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('status_delete', args=[self.status.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    def test_status_delete_protected(self):
        Task.objects.create(
            name='Protected Task',
            description='Task using status',
            status=self.status,
            creator=self.user
        )

        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('status_delete', args=[self.status.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
        self.assertIn(
            _("Невозможно удалить статус, используемый в задачах"),
            [msg.message for msg in response.wsgi_request._messages]
        )
