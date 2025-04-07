from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from task_manager.labels.models import Labels

class LabelTest(TestCase):

    def setUp(self):
        data_user = {
            "username": "volkovor777228",
            "first_name": "Lev",
            "last_name": "Smith",
            "password1": "1234",
            "password2": "1234",
        }
        self.client.post(reverse('users:create'), data_user)

        # Вход в систему с правильными данными
        self.client.login(username=data_user['username'], password='1234')

    
    def test_create(self):
        data_label = {
            "name": "enjoy"
        }
        response = self.client.post(reverse('labels:create'), data_label)
        self.assertRedirects(response, reverse('labels:list'))


        label = Labels.objects.get(name=data_label['name'])
        self.assertEqual(label.name, data_label['name'])
        
    def test_update(self):
        data_label = {
            "name": "enjoy"
        }
        self.client.post(reverse('labels:create'), data_label)
        label = Labels.objects.get(name=data_label['name'])

        self.assertEqual(label.name, data_label['name'])


        data_label_update = {
            "name": "Enjoys"
        }
        self.client.post(reverse('labels:update', args=[label.id]), data_label_update)
        label_new = Labels.objects.get(name=data_label_update['name'])
        self.assertEqual(label_new.name, data_label_update['name'])


    def test_delete(self):
        data_label = {
            "name": "enjoy"
        }
        self.client.post(reverse('labels:create'), data_label)
        label = Labels.objects.get(name=data_label['name'])

        self.assertEqual(label.name, data_label['name'])

        self.client.post(reverse('labels:delete', args=[label.id]))

        with self.assertRaises(ObjectDoesNotExist):
            Labels.objects.get(name=data_label['name'])

