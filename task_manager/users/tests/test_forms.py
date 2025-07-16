from task_manager.users.forms import CreateUserForm
from task_manager.users.tests.testcase import UsersTestCase


class UsersTestForms(UsersTestCase):
    def test_valid_data(self):
        form = CreateUserForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_missing_data(self):
        # Missing full data
        form = CreateUserForm(data={})
        self.assertFalse(form.is_valid())

        # Missing first_name and last_name
        data = self.valid_data.copy()
        data["first_name"] = ""
        data["last_name"] = ""
        form = CreateUserForm(data=data)
        self.assertTrue(form.is_valid())

        # Missing username
        data = self.valid_data.copy()
        data["username"] = ""
        form = CreateUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_unique_username_validation(self):
        data = self.valid_data.copy()
        data["username"] = self.user1.username
        form = CreateUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_username_too_long(self):
        long_username = "a" * 151
        data = self.valid_data.copy()
        data["username"] = long_username
        form = CreateUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_password_mismatch(self):
        data = self.valid_data.copy()
        data["confirm_password"] = "wrongpass"
        form = CreateUserForm(data=data)
        self.assertFalse(form.is_valid())

    def test_short_password(self):
        data = self.valid_data.copy()
        data["password"] = "ab"
        data["confirm_password"] = "ab"
        form = CreateUserForm(data=data)
        self.assertFalse(form.is_valid())
