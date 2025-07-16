from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.forms import LoginForm

User = get_user_model()


class LoginFormTest(TestCase):
    def test_valid_login(self):
        User.objects.create_user(username="testuser", password="testpassword")
        form_data = {"username": "testuser", "password": "testpassword"}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_empty_data(self):
        form_data = {}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)


class URLTests(TestCase):
    def test_index_view(self):
        # Проверка доступности главной страницы
        response = self.client.get(reverse_lazy("index"))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        # Проверка доступности страницы входа
        response = self.client.get(reverse_lazy("login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        # Проверка поведения при выходе (ожидается редирект)
        response = self.client.get(reverse_lazy("logout"))
        self.assertEqual(response.status_code, 302)


class HomePageTest(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse_lazy("index"))

    def test_home_page(self):
        # status_code
        self.assertEqual(self.response.status_code, 200)

        # template
        self.assertTemplateUsed(self.response, "index.html")

        # contains correct html
        self.assertContains(self.response, "Greetings from Hexlet!")

        # does not contain incorrect html
        self.assertNotContains(self.response, "This text shouldn't be here")
