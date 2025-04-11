from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from yaml import CLoader, load

from task_manager.statuses.models import Status

User = get_user_model()
path = (
    Path(__file__)
    .resolve()
    .parent.parent.joinpath("fixtures", "test_values.yaml")
)


class StatusTestCase(TestCase):
    fixtures = ["statuses.yaml"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(id=2)
        self.status1 = Status.objects.get(id=1)
        self.status2 = Status.objects.get(id=2)
        self.status_count = Status.objects.count()
        with path.open() as f:
            self.data = load(f, Loader=CLoader)
        self.valid_data = self.data.get("new_status")
        self.update_data = self.data.get("update_status")


class StatusViewsTest(StatusTestCase):
    def test_statuses_list(self):
        # user not authenticated
        response = self.client.get(reverse("statuses_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("statuses_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/statuses_list.html")
        self.assertEqual(Status.objects.count(), self.status_count)

    def test_create_status(self):
        # user not authenticated
        response = self.client.get(reverse("status_create"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        response = self.client.post(
            reverse("status_create"),
            self.valid_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("status_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")

        response = self.client.post(
            reverse("status_create"),
            self.valid_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), self.status_count + 1)
        self.assertEqual(
            Status.objects.filter(pk=self.status_count + 1)[0].name,
            self.valid_data.get("name"),
        )
        self.assertRedirects(response, reverse("statuses_list"))

    def test_update_status(self):
        # user not authenticated
        id = self.status1.id
        response = self.client.get(reverse("status_update", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        response = self.client.post(
            reverse("status_update", args=[id]), self.update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("status_update", args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")

        response = self.client.post(
            reverse("status_update", args=[id]), self.update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("statuses_list"))
        self.assertEqual(
            Status.objects.get(id=id).name,
            self.update_data.get("name"),
        )

    def test_delete_status(self):
        # user not authenticated
        id = self.status1.id
        response = self.client.get(reverse("status_delete", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        response = self.client.post(reverse("status_delete", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("status_delete", args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete.html")

        response = self.client.post(reverse("status_delete", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("statuses_list"))
        self.assertEqual(Status.objects.count(), self.status_count - 1)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(id=id)
