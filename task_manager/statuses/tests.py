from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from task_manager.statuses.models import Statuses


class StatusTest(TestCase):

    def setUp(self):
        data_user = {
            "username": "volkovor777228",
            "first_name": "Lev",
            "last_name": "Smith",
            "password1": "1234",
            "password2": "1234",
        }
        self.client.post(reverse("users:create"), data_user)

        # Вход в систему с правильными данными
        self.client.login(username=data_user["username"], password="1234")

    def test_create(self):
        data_status = {"name": "enjoy"}
        response = self.client.post(reverse("statuses:create"), data_status)
        self.assertRedirects(response, reverse("statuses:list"))

        status = Statuses.objects.get(name=data_status["name"])
        self.assertEqual(status.name, data_status["name"])

    def test_update(self):
        data_status = {"name": "enjoy"}
        self.client.post(reverse("statuses:create"), data_status)
        status = Statuses.objects.get(name=data_status["name"])

        self.assertEqual(status.name, data_status["name"])

        data_status_update = {"name": "Enjoys"}
        self.client.post(
            reverse("statuses:update", args=[status.id]), data_status_update
        )
        status_new = Statuses.objects.get(name=data_status_update["name"])
        self.assertEqual(status_new.name, data_status_update["name"])

    def test_delete(self):
        data_status = {"name": "enjoy"}
        self.client.post(reverse("statuses:create"), data_status)
        status = Statuses.objects.get(name=data_status["name"])

        self.assertEqual(status.name, data_status["name"])

        self.client.post(reverse("statuses:delete", args=[status.id]))

        with self.assertRaises(ObjectDoesNotExist):
            Statuses.objects.get(name=data_status["name"])
