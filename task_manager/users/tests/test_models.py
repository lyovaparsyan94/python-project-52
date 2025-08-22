from django.db import IntegrityError

from task_manager.users.models import User
from task_manager.users.tests.testcase import UserTestCase


class TestUsersModel(UserTestCase):
    def setUp(self):
        super().setUp()
        del self.valid_data["password2"]

    def test_user_creation(self):
        initial_count = User.objects.count()
        data = {
            "username": self.valid_data["username"],
            "password": self.valid_data["password1"],
        }
        User.objects.create_user(**data)
        self.assertEqual(User.objects.count(), initial_count + 1)

    def test_user_duplicate_username(self):
        data = {
            "username": self.user1.username,
            "password": self.valid_data["password1"],
        }
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**data)

    def test_status_missing_name(self):
        data = {
            "username": "",
            "password": self.valid_data["password1"],
        }
        with self.assertRaises(ValueError):
            User.objects.create_user(**data)
