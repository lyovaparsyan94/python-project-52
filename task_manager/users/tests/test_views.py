from django.urls import reverse_lazy

from task_manager.users.models import Users
from task_manager.users.tests.testcase import UsersTestCase


class UsersTestViews(UsersTestCase):
    def test_index_user_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse_lazy("users"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/index.html")
        self.assertIn("users", response.context)

    def test_create_user_view_get(self):
        response = self.client.get(reverse_lazy("create_user"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/create.html")

    def test_create_user_view_post_valid(self):
        response = self.client.post(
            reverse_lazy("create_user"), data=self.valid_data
        )
        self.assertRedirects(response, reverse_lazy("login"))
        self.assertTrue(
            Users.objects.filter(username=self.valid_data["username"]).exists()
        )

    def test_create_user_view_post_invalid(self):
        invalid_data = self.valid_data.copy()
        invalid_data["confirm_password"] = "WrongPass123"
        response = self.client.post(
            reverse_lazy("create_user"), data=invalid_data
        )
        self.assertEqual(response.status_code, 200)

    def test_update_user_view_get(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse_lazy("update_user", args=[self.user1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/update.html")

    def test_update_user_view_post_success(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse_lazy("update_user", args=[self.user1.id]),
            data=self.valid_data,
        )
        self.assertRedirects(response, reverse_lazy("users"))
        user = Users.objects.get(id=self.user1.id)
        self.assertEqual(user.first_name, self.valid_data["first_name"]),

    def test_update_user_permission_denied(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse_lazy("update_user", args=[self.user2.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_user_view_get(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse_lazy("delete_user", args=[self.user1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/delete.html")

    def test_delete_user_with_tasks(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse_lazy("delete_user", args=[self.user1.id])
        )
        self.assertEqual(response.status_code, 302)
