from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Statuses


class StatusWorkflowTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(
            first_name="John",
            last_name='Doe',
            username="piggiboy",
            password='111'
        )
        self.status = Statuses.objects.create(name='status')

    def test_create(self):
        response = self.client.get(reverse('create_status'))
        self.assertEqual(response.status_code, 302)
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_status'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "status")

    def test_update(self):
        self.client.force_login(self.user)
        url = reverse('update_status', kwargs={'pk': self.status.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, {'name': 'Updated'})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated')

    def test_delete(self):
        self.client.force_login(self.user)
        delete_url = reverse('delete_status', kwargs={'pk': self.status.pk})
        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status'))

        with self.assertRaises(Statuses.DoesNotExist):
            Statuses.objects.get(pk=self.status.pk)


class StatusAuthTests(TestCase):
    def test_anonymous_redirect(self):
        urls = [
            reverse('status'),
            reverse('create_status'),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('login/', response.url)
