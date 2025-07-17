from django.urls import reverse_lazy

from task_manager.labels.models import Labels
from task_manager.labels.tests.testcase import LabelsTestCase


class LabelsTestViews(LabelsTestCase):
    def test_labels_unauthenticated(self):
        response = self.client.get(reverse_lazy("labels"))
        self.assertRedirects(response, reverse_lazy("login"))

    def test_labels_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("labels"))
        self.assertTemplateUsed(response, "labels/index.html")


class LabelTestCreateView(LabelsTestCase):
    def test_label_creation_authorized(self):
        self.client.force_login(self.user)
        initial_count = Labels.objects.count()

        response = self.client.get(reverse_lazy("create_label"))
        self.assertTemplateUsed(response, "labels/create.html")

        response = self.client.post(
            reverse_lazy("create_label"),
            data=self.valid_data,
        )
        self.assertRedirects(response, reverse_lazy("labels"))
        self.assertEqual(Labels.objects.count(), initial_count + 1)

    def test_label_creation_unauthorized(self):
        response = self.client.get(reverse_lazy("create_label"))
        self.assertRedirects(response, reverse_lazy("login"))

        response = self.client.post(
            reverse_lazy("create_label"),
            data=self.valid_data,
        )
        self.assertRedirects(response, reverse_lazy("login"))


class LabelTestUpdateView(LabelsTestCase):
    def test_label_update_authorized(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy("update_label", kwargs={"pk": self.label.id})
        )
        self.assertTemplateUsed(response, "labels/update.html")

        response = self.client.post(
            reverse_lazy("update_label", kwargs={"pk": self.label.id}),
            data=self.update_data,
        )
        self.assertRedirects(response, reverse_lazy("labels"))
        updated_label = Labels.objects.get(id=self.label.id)
        self.assertEqual(updated_label.name, self.update_data["name"])

    def test_label_update_unauthorized(self):
        response = self.client.get(
            reverse_lazy("update_label", kwargs={"pk": self.label.id})
        )
        self.assertRedirects(response, reverse_lazy("login"))

        response = self.client.post(
            reverse_lazy("update_label", kwargs={"pk": self.label.id}),
            data=self.update_data,
        )
        self.assertRedirects(response, reverse_lazy("login"))


class LabelTestDeleteView(LabelsTestCase):
    def test_label_delete_authorized(self):
        self.client.force_login(self.user)
        initial_count = Labels.objects.count()

        response = self.client.get(
            reverse_lazy("delete_label", kwargs={"pk": self.label.id})
        )
        self.assertTemplateUsed(response, "labels/delete.html")

        response = self.client.post(
            reverse_lazy("delete_label", kwargs={"pk": self.label.id})
        )
        self.assertRedirects(response, reverse_lazy("labels"))
        self.assertEqual(Labels.objects.count(), initial_count - 1)

    def test_label_delete_unauthorized(self):
        response = self.client.get(
            reverse_lazy("delete_label", kwargs={"pk": self.label.id})
        )
        self.assertRedirects(response, reverse_lazy("login"))

        response = self.client.post(
            reverse_lazy("delete_label", kwargs={"pk": self.label.id})
        )
        self.assertRedirects(response, reverse_lazy("login"))
