from django.test import TestCase
from django.urls import reverse
from task_manager.models import Status
from django.contrib.auth.models import User

class StatusTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_status_create(self):
        self.client.login(username='test', password='test')
        self.client.post(reverse('statuses:create'), {'name': 'Новый'})
        self.assertEqual(Status.objects.count(), 1)
