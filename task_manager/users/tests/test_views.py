from django.urls import reverse_lazy

from task_manager.users.models import User
from task_manager.users.tests.testcase import UserTestCase


class UsersTestViews(UserTestCase):
    def test_index_user_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse_lazy("users:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/index.html")
        self.assertIn("users", response.context)

    def test_create_user_view_get(self):
        response = self.client.get(reverse_lazy("users:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/create.html")

    def test_create_user_view_post_valid(self):
        response = self.client.post(
            reverse_lazy("users:create"), data=self.valid_data
        )
        self.assertRedirects(response, reverse_lazy("login"))
        self.assertTrue(
            User.objects.filter(username=self.valid_data["username"]).exists()
        )

    def test_create_user_view_post_invalid(self):
        invalid_data = self.valid_data.copy()
        invalid_data["password2"] = "WrongPass123"
        response = self.client.post(
            reverse_lazy("users:create"), data=invalid_data
        )
        self.assertEqual(response.status_code, 200)

    def test_update_user_view_get(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse_lazy("users:update", args=[self.user1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/update.html")

    def test_update_user_view_post_success(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse_lazy("users:update", args=[self.user1.pk]),
            data=self.valid_data,
        )
        self.assertRedirects(response, reverse_lazy("users:index"))
        user = User.objects.get(id=self.user1.pk)
        self.assertEqual(user.first_name, self.valid_data["first_name"]),

    def test_update_user_permission_denied(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse_lazy("users:update", args=[self.user2.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_user_view_get(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse_lazy("users:delete", args=[self.user1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/delete.html")

    def test_delete_user_with_tasks(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse_lazy("users:delete", args=[self.user1.pk])
        )
        self.assertEqual(response.status_code, 302)
