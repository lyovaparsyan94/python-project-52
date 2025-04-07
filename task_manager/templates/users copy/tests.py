from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


class UserTest(TestCase):
    
    def test_create(self):
        data_user = {
            "username": "volkovor777228",
            "first_name": "Lev",
            "last_name": "Smith",
            "password1": "1234",
            "password2": "1234",

        }
        response = self.client.post(reverse('users:create'), data_user)
        self.assertRedirects(response, reverse('login'))

        # Проверка, что пользователь был создан
        User = get_user_model()
        self.assertTrue(User.objects.filter(username="volkovor777228").exists())
        
    def test_update(self):
        # Создание пользователя
        data_user = {
            "username": "volkovor777228",
            "first_name": "Lev",
            "last_name": "Smith",
            "password1": "1234",
            "password2": "1234",
        }
        response = self.client.post(reverse('users:create'), data_user)

        # Вход в систему с правильными данными
        self.client.login(username=data_user['username'], password='1234')

        # Обновление данных пользователя
        data_user_update = {
            "username": "volkovor777228",
            "first_name": "Lev228",
            "last_name": "Smith777",
            "password1": "1234",
            "password2": "1234",
        }
        user = get_user_model().objects.get(username=data_user['username'])
        response = self.client.post(reverse('users:update', args=[user.id]), data_user_update)

        # Проверка перенаправления
        self.assertRedirects(response, reverse('users:list'))

    def test_delete(self):
        data_user = {
            "username": "volkovor777228",
            "first_name": "Lev228",
            "last_name": "Smith777",
            "password1": "1234",
            "password2": "1234",
        }
        response = self.client.post(reverse('users:create'), data_user)
        self.client.login(username=data_user['username'], password='1234')
        user = get_user_model().objects.get(username=data_user['username'])
        response = self.client.post(reverse('users:delete', args=[user.id]))
        self.assertRedirects(response, reverse('users:list'))
        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.get(username=data_user['username'])

    def test_read(self):
        data_user = {
            "username": "volkovor777228",
            "first_name": "Lev228",
            "last_name": "Smith777",
            "password1": "1234",
            "password2": "1234",
        }
        self.client.post(reverse('users:create'), data_user)
        user = get_user_model().objects.get(username=data_user['username'])
        self.assertEqual(user.first_name, data_user['first_name'])
        self.assertEqual(user.last_name, data_user['last_name'])
        self.assertEqual(user.username, data_user['username'])
