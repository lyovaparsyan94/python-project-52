from django.test import Client, TestCase

from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        status = {"name": "inwork", "created_at": "2023-08-11T17:04:28.819Z"}
        user = {
            "first_name": "John",
            "last_name": "Snow",
            "username": "john_snow",
            "password": "Stark123",
        }

        self.status = Status.objects.create(**status)
        self.user = User.objects.create(**user)

        self.valid_data = {"name": "Test Status"}

        self.update_data = {"name": "Updated Status"}
