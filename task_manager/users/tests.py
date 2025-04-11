from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from yaml import CLoader, load

User = get_user_model()
path = (
    Path(__file__)
    .resolve()
    .parent.parent.joinpath("fixtures", "test_values.yaml")
)


class UserTestCase(TestCase):
    fixtures = ["users.yaml"]

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)
        self.user_count = User.objects.count()
        with path.open() as f:
            self.data = load(f, Loader=CLoader)
        self.valid_data = self.data.get("new_user")
        self.update_data = self.data.get("update_user")


class UserViewsTest(UserTestCase):
    def test_users_list(self):
        response = self.client.get(reverse("users_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/users_list.html")
        self.assertEqual(User.objects.count(), self.user_count)

    def test_create_user(self):
        response = self.client.get(reverse("user_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")

        response = self.client.post(
            reverse("user_create"),
            self.valid_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), self.user_count + 1)
        self.assertEqual(
            User.objects.filter(pk=self.user_count + 1)[0].username,
            self.valid_data.get("username"),
        )
        self.assertRedirects(response, reverse("login"))

    def test_update_user(self):
        # user not authenticated
        user1 = self.user1
        response = self.client.get(reverse("user_update", args=[user1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        response = self.client.post(reverse("user_update", args=[user1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        user2 = self.user2
        self.client.force_login(user2)
        response = self.client.get(reverse("user_update", args=[user2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")

        response = self.client.post(
            reverse("user_update", args=[user2.id]), self.update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))
        updated_user = User.objects.get(id=user2.id)
        self.assertEqual(
            updated_user.username, self.update_data.get("username")
        )
        self.assertEqual(updated_user.email, self.update_data.get("email"))

        # user is authenticated, but tried to update another user
        response = self.client.get(reverse("user_update", args=[user1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))

        response = self.client.post(
            reverse("user_update", args=[user1.id]), self.update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))
        self.assertNotEqual(user1.username, self.update_data.get("username"))

    def test_delete_user(self):
        # user not authenticated
        user1 = self.user1
        response = self.client.get(reverse("user_delete", args=[user1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        response = self.client.post(reverse("user_delete", args=[user1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        user2 = self.user2
        self.client.force_login(user2)
        response = self.client.get(reverse("user_delete", args=[user2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete.html")

        response = self.client.post(reverse("user_delete", args=[user2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))
        self.assertEqual(User.objects.count(), self.user_count - 1)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user2.id)

        # user is authenticated, but tried to delete another user
        self.client.force_login(user1)
        response = self.client.get(
            reverse("user_delete", args=[self.user_count])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))

        response = self.client.post(
            reverse("user_delete", args=[self.user_count])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))
        self.assertEqual(User.objects.count(), self.user_count - 1)
