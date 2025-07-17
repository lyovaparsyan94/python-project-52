from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from .models import Label


# Create your tests here.
class LabelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="user",
            password="password"
        )
        self.client.force_login(self.user)

    def test_create(self):
        data_label = {
            'name': 'create'
        }
        response = self.client.post(reverse('label_create'), data_label)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='create').exists())

    def test_update_statuses(self):
        data_label = {
            'name': 'create'
        }
        self.client.post(reverse('label_create'), data_label)

        label = Label.objects.get(name=data_label['name'])
        update_data = {'name': 'createpof'}
        response = self.client.post(reverse(
            'label_update', args=[label.id]), update_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='createpof').exists())

    def test_delete_statuses(self):
        data_label = {
            'name': 'create'
        }
        self.client.post(reverse('label_create'), data_label)
        label = Label.objects.get(name=data_label['name'])
        self.client.post(reverse('label_delete', args=[label.id]))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(name=data_label["name"])
