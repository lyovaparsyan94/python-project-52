from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages


class UserTest(TestCase):
    def setUp(self):
        User = get_user_model()
        # Создаем тестовых пользователей
        User.objects.create_user(
            username='testuser1',
            password='testpass123',
            first_name='Test',
            last_name='User1',
            email='testuser1@example.com'
        )
        User.objects.create_user(
            username='testuser2',
            password='testpass123',
            first_name='Test',
            last_name='User2',
            email='testuser2@example.com'
        )
        User.objects.create_user(
            username='testuser3',
            password='testpass123',
            first_name='Test',
            last_name='User3',
            email='testuser3@example.com'
        )

    def test_load_users(self):
        User = get_user_model()
        users = User.objects.all()
        self.assertEqual(len(users), 3)

    def test_create_user(self):
        user_data = {
            'username': 'testuser',
            'first_name': 'user',
            'last_name': 'userov',
            'password1': 'stronGpassw123',
            'password2': 'stronGpassw123',
        }

        response = self.client.post(reverse('users:create'), user_data)
        self.assertRedirects(response, reverse('login'))

        User = get_user_model()
        user = User.objects.get(username=user_data['username'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])

    def test_update_user(self):
        user_data = {
            'username': 'testuser',
            'first_name': 'user',
            'last_name': 'userov',
            'password1': 'stronGpassw123',
            'password2': 'stronGpassw123',
        }

        self.client.post(reverse('users:create'), user_data)
        self.client.login(
            username=user_data['username'],
            password=user_data['password1']
        )

        update_user_data = {
            'username': 'testuser',
            'first_name': 'userupd',
            'last_name': 'userovupd',
            'password1': 'stronGpassw123',
            'password2': 'stronGpassw123',
        }

        User = get_user_model()
        user = User.objects.get(username=user_data['username'])
        response = self.client.post(
            reverse('users:update', args=[user.id]), update_user_data
        )

        user.refresh_from_db()

        self.assertRedirects(response, reverse('users:users'))
        self.assertEqual(user.first_name, update_user_data['first_name'])
        self.assertEqual(user.last_name, update_user_data['last_name'])

    def test_read_user(self):
        user_data = {
            'username': 'testuser',
            'first_name': 'userupd',
            'last_name': 'userovupd',
            'password1': 'stronGpassw123',
            'password2': 'stronGpassw123',
        }

        self.client.post(reverse('users:create'), user_data)

        User = get_user_model()
        user = User.objects.get(username=user_data['username'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])

    def test_delete_user(self):
        user_data = {
            'username': 'testuser',
            'first_name': 'userupd',
            'last_name': 'userovupd',
            'password1': 'stronGpassw123',
            'password2': 'stronGpassw123',
        }

        response = self.client.post(reverse('users:create'), user_data)
        self.client.login(
            username=user_data['username'],
            password=user_data['password1']
        )
        User = get_user_model()
        user = User.objects.get(username=user_data['username'])
        response = self.client.post(reverse('users:delete', args=[user.id]))
        self.assertRedirects(response, reverse('users:users'))

    def test_permissions_user(self):
        user1_data = {
            'username': 'testuser1',
            'first_name': 'user1',
            'last_name': 'userov1',
            'password1': 'stronGpassw1231',
            'password2': 'stronGpassw1231',
        }

        user2_data = {
            'username': 'testuser2',
            'first_name': 'user2',
            'last_name': 'userov2',
            'password1': 'stronGpassw1232',
            'password2': 'stronGpassw1232',
        }

        response = self.client.post(reverse('users:create'), user1_data)
        response = self.client.post(reverse('users:create'), user2_data)

        self.client.login(
            username=user1_data['username'],
            password=user1_data['password1']
        )

        update_user_data = {
            'username': 'testuser3',
            'first_name': 'user3',
            'last_name': 'userov3',
            'password1': 'stronGpassw1233',
            'password2': 'stronGpassw1233',
        }

        User = get_user_model()
        user = User.objects.get(username=user2_data['username'])
        response = self.client.post(
            reverse('users:update', args=[user.id]), update_user_data
        )

        self.assertRedirects(response, reverse('users:users'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 3)
        self.assertIn('Пользователь успешно зарегистрирован', str(messages[0]))
        self.assertIn('Пользователь успешно зарегистрирован', str(messages[1]))
        self.assertIn(
            'У вас нет прав для изменения другого пользователя.',
            str(messages[2])
        )

        self.assertEqual(user.first_name, 'user2')
        self.assertEqual(user.last_name, 'userov2')

    def test_user_logout(self):
        user_data = {
            'username': 'testuser',
            'first_name': 'user',
            'last_name': 'userov',
            'password1': 'stronGpassw123',
            'password2': 'stronGpassw123',
        }

        self.client.post(reverse('users:create'), user_data)
        self.client.login(
            username=user_data['username'],
            password=user_data['password1']
        )

        response = self.client.get(reverse('logout'))

        self.assertRedirects(response, reverse('index'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertIn('Вы разлогинены', str(messages[1])) 