from django.urls import reverse_lazy

from task_manager.statuses.models import Status
from task_manager.statuses.tests.testcase import StatusTestCase


class StatusTestViews(StatusTestCase):
    def test_labels_unauthenticated(self):
        response = self.client.get(reverse_lazy("statuses:index"))
        self.assertRedirects(response, reverse_lazy("login"))

    def test_labels_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("statuses:index"))
        self.assertTemplateUsed(response, "statuses/index.html")


class StatusTestCreateView(StatusTestCase):
    def test_status_creation_authorized(self):
        self.client.force_login(self.user)
        initial_count = Status.objects.count()

        response = self.client.get(reverse_lazy("statuses:create"))
        self.assertTemplateUsed(response, "statuses/create.html")

        response = self.client.post(
            reverse_lazy("statuses:create"),
            data=self.valid_data,
        )
        self.assertRedirects(response, reverse_lazy("statuses:index"))
        self.assertEqual(Status.objects.count(), initial_count + 1)

    def test_status_creation_unauthorized(self):
        response = self.client.get(reverse_lazy("statuses:create"))
        self.assertRedirects(response, reverse_lazy("login"))

        response = self.client.post(
            reverse_lazy("statuses:create"),
            data=self.valid_data,
        )
        self.assertRedirects(response, reverse_lazy("login"))


class StatusTestUpdateView(StatusTestCase):
    def test_status_update_authorized(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy("statuses:update", kwargs={"pk": self.status.id})
        )
        self.assertTemplateUsed(response, "statuses/update.html")

        response = self.client.post(
            reverse_lazy("statuses:update", kwargs={"pk": self.status.id}),
            data=self.update_data,
        )
        self.assertRedirects(response, reverse_lazy("statuses:index"))
        updated_status = Status.objects.get(id=self.status.id)
        self.assertEqual(updated_status.name, self.update_data["name"])

    def test_status_update_unauthorized(self):
        response = self.client.get(
            reverse_lazy("statuses:update", kwargs={"pk": self.status.id})
        )
        self.assertRedirects(response, reverse_lazy("login"))

        response = self.client.post(
            reverse_lazy("statuses:update", kwargs={"pk": self.status.id}),
            data=self.update_data,
        )
        self.assertRedirects(response, reverse_lazy("login"))


class StatusTestDeleteView(StatusTestCase):
    def test_status_delete_authorized(self):
        self.client.force_login(self.user)
        initial_count = Status.objects.count()

        response = self.client.get(
            reverse_lazy("statuses:delete", kwargs={"pk": self.status.id})
        )
        self.assertTemplateUsed(response, "statuses/delete.html")

        response = self.client.post(
            reverse_lazy("statuses:delete", kwargs={"pk": self.status.id})
        )
        self.assertRedirects(response, reverse_lazy("statuses:index"))
        self.assertEqual(Status.objects.count(), initial_count - 1)

    def test_status_delete_unauthorized(self):
        response = self.client.get(
            reverse_lazy("statuses:delete", kwargs={"pk": self.status.id})
        )
        self.assertRedirects(response, reverse_lazy("login"))

        response = self.client.post(
            reverse_lazy("statuses:delete", kwargs={"pk": self.status.id})
        )
        self.assertRedirects(response, reverse_lazy("login"))
