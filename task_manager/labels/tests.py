from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from yaml import CLoader, load

from task_manager.labels.models import Label

User = get_user_model()
path = (
    Path(__file__)
    .resolve()
    .parent.parent.joinpath("fixtures", "test_values.yaml")
)


class LabelTestCase(TestCase):
    fixtures = ["labels.yaml"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(id=2)
        self.label1 = Label.objects.get(id=1)
        self.label2 = Label.objects.get(id=2)
        self.count = Label.objects.count()
        with path.open() as f:
            self.data = load(f, Loader=CLoader)
        self.valid_data = self.data.get("new_label")
        self.update_data = self.data.get("update_label")


class LabelViewsTest(LabelTestCase):
    def test_labels_list(self):
        # user not authenticated
        response = self.client.get(reverse("labels_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("labels_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels_list.html")
        self.assertEqual(Label.objects.count(), self.count)

    def test_create_label(self):
        # user not authenticated
        response = self.client.get(reverse("label_create"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        response = self.client.post(
            reverse("label_create"),
            self.valid_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("label_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")

        response = self.client.post(
            reverse("label_create"),
            self.valid_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels_list"))
        self.assertEqual(Label.objects.count(), self.count + 1)
        self.assertEqual(
            Label.objects.filter(pk=self.count + 1)[0].name,
            self.valid_data.get("name"),
        )

    def test_update_label(self):
        # user not authenticated
        id = self.label1.id
        response = self.client.get(reverse("label_update", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        response = self.client.post(
            reverse("label_update", args=[id]), self.update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("label_update", args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")

        response = self.client.post(
            reverse("label_update", args=[id]), self.update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels_list"))
        self.assertEqual(
            Label.objects.get(id=id).name,
            self.update_data.get("name"),
        )

    def test_delete_label(self):
        # user not authenticated
        id = self.label1.id
        response = self.client.get(reverse("label_delete", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        response = self.client.post(reverse("label_delete", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("label_delete", args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete.html")

        response = self.client.post(reverse("label_delete", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels_list"))
        self.assertEqual(Label.objects.count(), self.count - 1)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(id=id)

        # user is authenticated, but label used by task
        id = self.label2.id
        response = self.client.get(reverse("label_delete", args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete.html")

        response = self.client.post(reverse("label_delete", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("labels_list"))
        self.assertEqual(Label.objects.count(), self.count - 1)
        self.assertEqual(Label.objects.get(id=id).name, self.label2.name)
