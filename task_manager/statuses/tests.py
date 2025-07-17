from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from .models import Status


# Create your tests here.
class StatusTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="user1",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_create(self):
        data_status = {
            'name': 'create'
        }
        response = self.client.post(reverse('status_create'), data_status)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='create').exists())

    def test_update_statuses(self):
        data_status = {
            'name': 'create'
        }
        self.client.post(reverse('status_create'), data_status)

        status = Status.objects.get(name=data_status['name'])
        update_data = {'name': 'createpof'}
        response = self.client.post(reverse(
            'status_update', args=[status.id]), update_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='createpof').exists())

    def test_delete_statuses(self):
        data_status = {
            'name': 'create'
        }
        self.client.post(reverse('status_create'), data_status)
        status = Status.objects.get(name=data_status['name'])
        self.client.post(reverse('status_delete', args=[status.id]))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(name=data_status["name"])
