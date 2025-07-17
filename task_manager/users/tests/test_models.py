from django.core.exceptions import ValidationError
from django.db import IntegrityError

from task_manager.users.models import Users
from task_manager.users.tests.testcase import UsersTestCase


class TestUsersModel(UsersTestCase):
    def setUp(self):
        super().setUp()
        del self.valid_data["confirm_password"]

    def test_user_creation(self):
        initial_count = Users.objects.count()
        Users.objects.create(**self.valid_data)
        self.assertEqual(Users.objects.count(), initial_count + 1)

    def test_user_duplicate_username(self):
        data = self.valid_data.copy()
        data["username"] = self.user1.username
        with self.assertRaises(IntegrityError):
            Users.objects.create(**data)

    def test_status_missing_name(self):
        data = self.valid_data.copy()
        data["username"] = ""
        user = Users.objects.create(**data)
        with self.assertRaises(ValidationError):
            user.full_clean()
