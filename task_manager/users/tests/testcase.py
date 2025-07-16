from django.test import Client, TestCase

from task_manager.users.models import User


class UserTestCase(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)

        self.valid_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "password": "testpass123",
            "confirm_password": "testpass123",
        }

        self.update_data = {
            "first_name": "Updated",
            "last_name": "User",
            "username": "updateduser",
            "password": "updatedpass123",
            "confirm_password": "updatedpass123",
        }
