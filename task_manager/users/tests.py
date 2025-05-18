from django.test import TestCase
from django.contrib.auth import get_user_model


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