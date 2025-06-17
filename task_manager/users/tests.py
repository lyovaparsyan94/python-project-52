from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserTests(TestCase):
    fixtures = ['data.json']

    def setUp(self):

        self.test_user = User.objects.filter(username='happylarry')[0]
        self.test_user2 = User.objects.filter(username='harry777')[0]
        self.test_user3 = User.objects.filter(username='testuser')[0]

    def test_create(self):
        data = {
            'username': 'frstgmp',
            'password1': '12345',
            'password2': '12345',
            'first_name': 'Forest',
            'last_name': 'Gump',
        }
        response = self.client.post(reverse('users:create_user'),
                                    data,
                                    follow=True)

        self.assertRedirects(response, reverse('login'))

        self.assertTrue(User.objects.filter(
            username='frstgmp', is_active=True).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]),
                         'Пользователь успешно зарегистрирован')

    def test_update(self):
        self.client.login(
            username='happylarry', password='123')
        url = reverse('users:update_user', kwargs={'id': self.test_user.pk})

        data = {
            'username': 'usr1_1',
            'password1': 'pass2',
            'password2': 'pass2',
            'first_name': 'UptdMy',
            'last_name': 'UptdName'
        }

        response = self.client.post(url, data, follow=True)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, 'usr1_1')
        self.assertEqual(self.test_user.first_name, 'UptdMy')
        self.assertEqual(self.test_user.last_name, 'UptdName')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно изменен')

    def test_GET_delete(self):
        self.client.login(username='happylarry', password='123')
        url = reverse('users:delete_user', kwargs={'id': self.test_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_POST_delete(self):
        self.client.login(username='testuser', password='123')
        url = reverse('users:delete_user', kwargs={'id': self.test_user3.pk})
        response = self.client.post(url, follow=True)
        self.assertFalse(User.objects.filter(username='testuser').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно удален')
        self.assertRedirects(response, reverse('users:users'))

    def test_user_invalid_permissions_update(self):
        self.client.login(username='happylarry', password='123')
        url = reverse('users:update_user', kwargs={'id': self.test_user2.pk})
        response = self.client.post(url, {
            'username': 'abcdef',
            'password1': 'def123',
            'password2': 'def123',
            'first_name': 'abc',
            'last_name': 'def'
        })
        self.assertRedirects(response, reverse('users:users'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'У вас нет прав\
                        для изменения другого пользователя.')

