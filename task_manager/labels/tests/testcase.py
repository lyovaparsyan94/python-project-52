from django.test import Client, TestCase

from task_manager.labels.models import Label
from task_manager.users.models import User


class LabelTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        label = {"name": "bug", "created_at": "2023-09-24T16:06:44.864685Z"}
        user = {
            "first_name": "John",
            "last_name": "Snow",
            "username": "john_snow",
            "password": "Stark123",
        }

        self.label = Label.objects.create(**label)
        self.user = User.objects.create(**user)

        self.valid_data = {
            "name": "Test Label",
        }

        self.update_data = {
            "name": "Updated Label",
        }
