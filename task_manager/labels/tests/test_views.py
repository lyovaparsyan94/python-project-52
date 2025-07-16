from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _

from task_manager.labels.models import Label
from task_manager.users.models import User

from .testcase import LabelTestCase


class LabelViewsTest(LabelTestCase):
    def test_label_list_requires_login(self):
        response = self.client.get(reverse('labels_list'))
        self.assertRedirects(
            response,
            f'/{translation.get_language()}/login/?next=/{translation.get_language()}/labels/'
        )

    def test_label_create(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('label_create'),
            self.label_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_delete_protected(self):
        self.task.labels.add(self.label)
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('label_delete', args=[self.label.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
        self.assertIn(
            _("Невозможно удалить метку, используемую в задачах"),
            [msg.message for msg in response.wsgi_request._messages]
        )

    def test_label_update(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('label_update', args=[self.label.pk]),
            {'name': 'Updated Label'}
        )
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_create_invalid(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('label_create'), 
            {'name': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)

    def test_label_delete_no_permission(self):
        User.objects.create_user(
            username='another', 
            password='testpass'
        )
        self.client.login(username='another', password='testpass')
        response = self.client.post(
            reverse('label_delete', args=[self.label.pk])
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
