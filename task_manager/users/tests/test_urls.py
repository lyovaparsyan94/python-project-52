from django.test import SimpleTestCase
from django.urls import resolve, reverse_lazy

from task_manager.users.views import (
    CreateUserView,
    DeleteUserView,
    IndexUserView,
    UpdateUserView,
)


class TestUserURLs(SimpleTestCase):
    """Тестирование маршрутов URL для пользователей."""

    def test_index_user_url(self):
        """Проверка маршрута для списка пользователей."""
        url = reverse_lazy("users")
        self.assertEqual(resolve(url).func.view_class, IndexUserView)

    def test_create_user_url(self):
        """Проверка маршрута для создания пользователя."""
        url = reverse_lazy("create_user")
        self.assertEqual(resolve(url).func.view_class, CreateUserView)

    def test_update_user_url(self):
        """Проверка маршрута для обновления пользователя."""
        url = reverse_lazy("update_user", args=[1])
        self.assertEqual(resolve(url).func.view_class, UpdateUserView)

    def test_delete_user_url(self):
        """Проверка маршрута для удаления пользователя."""
        url = reverse_lazy("delete_user", args=[1])
        self.assertEqual(resolve(url).func.view_class, DeleteUserView)
