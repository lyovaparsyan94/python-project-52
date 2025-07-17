import datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Status

User = get_user_model()


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="qwe123",
        )
        self.client.login(username="testuser", password="qwe123")
        self.status = Status.objects.create(name="Test Status")

    def test_create(self):
        """Тест создания статуса"""
        response = self.client.post(
            reverse("statuses:create"),
            {"name": "new1"},
        )
        self.assertEqual(response.status_code, 302)
        status = Status.objects.get(name="new1")
        self.assertIsInstance(status.created_at, datetime.datetime)

    def test_read(self):
        """Тест показа статуса"""
        response = self.client.get(reverse("statuses:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.name)

    def test_update_status(self):
        """Тест обновления статуса"""
        url = reverse("statuses:update", args=[self.status.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # POST запрос - отправка изменений
        new_name = "Updated Status"
        response = self.client.post(url, {"name": new_name})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("statuses:list"))

        # Проверяем обновление в БД
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, new_name)

        # Проверяем сообщение об успехе
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Статус успешно изменен")

    def test_delete_status(self):
        """Тест удаления статуса"""
        url = reverse("statuses:delete", args=[self.status.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # POST запрос - выполнение удаления
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("statuses:list"))

        # Проверяем удаление из БД
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

        # Проверяем сообщение об успехе
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Статус успешно удален")
