import pytest
from django.contrib.auth import get_user_model


class TestUser:
    @pytest.fixture(autouse=True)
    def setup(self, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
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

    def test_load_users(self, transactional_db, django_user_model):
        users = django_user_model.objects.all()
        assert len(users) == 3 