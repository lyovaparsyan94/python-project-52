
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.statuses.models import Status

User = get_user_model()


class StatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="test",
            last_name="test",
            username="TestUser",
            password="password123",
        )
        self.status = Status.objects.create(name="Test Status")
        self.status2 = Status.objects.create(name="Second Status")

        self.statuses_url = reverse_lazy("statuses_index")
        self.create_url = reverse_lazy("statuses_create")
        self.update_url = reverse_lazy(
            "statuses_update",
            kwargs={"pk": self.status.id})
        self.delete_url = reverse_lazy(
            "statuses_delete",
            kwargs={"pk": self.status.id})
        self.login_url = reverse_lazy("login")

    def test_status_list(self):
        response = self.client.get(self.statuses_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        self.client.login(username="TestUser", password="password123")
        response = self.client.get(self.statuses_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/index.html")
        self.assertContains(response, self.status.name)
        self.assertContains(response, self.status2.name)

        statuses = response.context["statuses"]
        self.assertEqual(len(statuses), 2)
        self.assertIn(self.status, statuses)
        self.assertIn(self.status2, statuses)

    def test_status_create(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        self.client.login(username="TestUser", password="password123")

        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general_form.html")

        response = self.client.post(self.create_url, {"name": "New Status"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.statuses_url)
        self.assertEqual(Status.objects.count(), 3)
        self.assertTrue(Status.objects.filter(name="New Status").exists())

        response = self.client.post(self.create_url, {"name": "Test Status"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), 3)

        response = self.client.post(self.create_url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), 3)

    def test_status_update_authorized(self):
        self.client.login(username="TestUser", password="password123")

        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general_form.html")

        response = self.client.post(
            self.update_url,
            {"name": "Updated Status"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.statuses_url)

        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated Status")

        response = self.client.post(self.update_url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated Status")

    def test_status_update_unauthorized(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        response = self.client.post(
            self.update_url,
            {"name": "Updated Status"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Test Status")

    def test_status_delete_authorized(self):
        self.client.login(username="TestUser", password="password123")

        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general_delete_form.html")

        self.assertTrue(Status.objects.filter(id=self.status.id).exists())

        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.statuses_url)

        self.assertEqual(Status.objects.count(), 1)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_status_delete_unauthorized(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        self.assertTrue(Status.objects.filter(id=self.status.id).exists())
        self.assertEqual(Status.objects.count(), 2)
