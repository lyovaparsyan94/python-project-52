from django.test import TestCase

from task_manager.users.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)


class UserFormsTest(TestCase):
    def test_user_creation_form_valid(self):
        form_data = {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'email': 'new@example.com'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_creation_form_invalid(self):
        form_data = {
            'username': '',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'email': 'invalid-email'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)

    def test_user_change_form_valid(self):
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        form = CustomUserChangeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_change_form_invalid(self):
        form_data = {
            'username': '',
            'email': 'invalid-email'
        }
        form = CustomUserChangeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
