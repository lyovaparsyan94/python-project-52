from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Labels


class StatusWorkflowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(
            first_name="John",
            last_name='Doe',
            username="piggiboy",
            password='111'
        )
        self.label = Labels.objects.create(name='label')

    def test_create(self):
        response = self.client.get(reverse('create_label'))
        self.assertEqual(response.status_code, 302)
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_label'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "labels")

    def test_update(self):
        self.client.force_login(self.user)
        url = reverse('update_label', kwargs={'pk': self.label.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, {'name': 'Updated'})
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated')

    def test_delete(self):
        self.client.force_login(self.user)
        delete_url = reverse('delete_label', kwargs={'pk': self.label.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels'))
        with self.assertRaises(Labels.DoesNotExist):
            Labels.objects.get(pk=self.label.pk)


class StatusAuthTests(TestCase):
    def test_anonymous_redirect(self):
        urls = [
            reverse('labels'),
            reverse('create_label'),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('login/', response.url)
