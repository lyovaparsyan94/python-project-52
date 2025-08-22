from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.labels.tests.testcase import LabelTestCase


class LabelsTestViews(LabelTestCase):
    def test_labels_unauthenticated(self):
        response = self.client.get(reverse_lazy("labels:index"))
        self.assertRedirects(response, reverse_lazy("login"))

    def test_labels_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("labels:index"))
        self.assertTemplateUsed(response, "labels/index.html")


class LabelTestCreateView(LabelTestCase):
    def test_label_creation_authorized(self):
        self.client.force_login(self.user)
        initial_count = Label.objects.count()

        response = self.client.get(reverse_lazy("labels:create"))
        self.assertTemplateUsed(response, "labels/create.html")

        response = self.client.post(
            reverse_lazy("labels:create"),
            data=self.valid_data,
        )
        self.assertRedirects(response, reverse_lazy("labels:index"))
        self.assertEqual(Label.objects.count(), initial_count + 1)

    def test_label_creation_unauthorized(self):
        response = self.client.get(reverse_lazy("labels:create"))
        self.assertRedirects(response, reverse_lazy("login"))

        response = self.client.post(
            reverse_lazy("labels:create"),
            data=self.valid_data,
        )
        self.assertRedirects(response, reverse_lazy("login"))


class LabelTestUpdateView(LabelTestCase):
    def test_label_update_authorized(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy("labels:update", kwargs={"pk": self.label.id})
        )
        self.assertTemplateUsed(response, "labels/update.html")

        response = self.client.post(
            reverse_lazy("labels:update", kwargs={"pk": self.label.id}),
            data=self.update_data,
        )
        self.assertRedirects(response, reverse_lazy("labels:index"))
        updated_label = Label.objects.get(id=self.label.id)
        self.assertEqual(updated_label.name, self.update_data["name"])

    def test_label_update_unauthorized(self):
        response = self.client.get(
            reverse_lazy("labels:update", kwargs={"pk": self.label.id})
        )
        self.assertRedirects(response, reverse_lazy("login"))

        response = self.client.post(
            reverse_lazy("labels:update", kwargs={"pk": self.label.id}),
            data=self.update_data,
        )
        self.assertRedirects(response, reverse_lazy("login"))


class LabelTestDeleteView(LabelTestCase):
    def test_label_delete_authorized(self):
        self.client.force_login(self.user)
        initial_count = Label.objects.count()

        response = self.client.get(
            reverse_lazy("labels:delete", kwargs={"pk": self.label.id})
        )
        self.assertTemplateUsed(response, "labels/delete.html")

        response = self.client.post(
            reverse_lazy("labels:delete", kwargs={"pk": self.label.id})
        )
        self.assertRedirects(response, reverse_lazy("labels:index"))
        self.assertEqual(Label.objects.count(), initial_count - 1)

    def test_label_delete_unauthorized(self):
        response = self.client.get(
            reverse_lazy("labels:delete", kwargs={"pk": self.label.id})
        )
        self.assertRedirects(response, reverse_lazy("login"))

        response = self.client.post(
            reverse_lazy("labels:delete", kwargs={"pk": self.label.id})
        )
        self.assertRedirects(response, reverse_lazy("login"))
