from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class UserTest(TestCase):
    def test_create(self):
        data_us = {
            'username': 'user1',
            'first_name': 'user_fname',
            'last_name': 'user_lname',
            'password1': 'qwa12',
            'password2': 'qwa12'
        }
        response = self.client.post(reverse('user_create'), data_us)
        self.assertEqual(response.status_code, 302)
        User = get_user_model()
        user = User.objects.get(username=data_us['username'])
        self.assertEqual(user.first_name, data_us['first_name'])
        self.assertEqual(user.last_name, data_us['last_name'])
    
    def test_update(self):
        data_us = {
            'username': 'user1',
            'first_name': 'user_fname',
            'last_name': 'user_lname',
            'password1': 'qwa12',
            'password2': 'qwa12'
        }
        self.client.post(reverse('user_create'), data_us)
        self.client.login(username=data_us['username'],
                          password=data_us['password1'])
        data_us_2 = {
            'username': 'user1',
            'first_name': 'user_fname',
            'last_name': 'user_lname',
            'password1': 'qwa12',
            'password2': 'qwa12'
        }
        
        User = get_user_model()
        user = User.objects.get(username=data_us['username'])
        response = self.client.post(reverse('user_update',
                                            args=[user.id]),
                                            data_us_2)
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, data_us_2['first_name'])
        self.assertEqual(user.last_name, data_us_2['last_name'])
        
    def test_delete(self):
        data_us = {
            'username': 'user1',
            'first_name': 'user_fname',
            'last_name': 'user_lname',
            'password1': 'qwa12',
            'password2': 'qwa12'
        }
        self.client.post(reverse('user_create'), data_us)
        self.client.login(username=data_us['username'],
                          password=data_us['password1'])
        User = get_user_model()
        user = User.objects.get(username=data_us['username'])
        response = self.client.post(reverse('user_delete', args=[user.id]))
        self.assertEqual(response.status_code, 302)
        users = User.objects.all()
        self.assertNotIn(user, users)