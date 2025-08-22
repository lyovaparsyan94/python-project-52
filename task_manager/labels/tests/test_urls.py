from django.urls import reverse_lazy

from task_manager.labels.tests.testcase import LabelTestCase


class LabelTestUrl(LabelTestCase):
    def test_label_unauthorized(self):
        response = self.client.get(reverse_lazy("labels:index"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse_lazy("labels:create"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse_lazy("labels:update", kwargs={"pk": self.label.id})
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse_lazy("labels:delete", kwargs={"pk": self.label.id})
        )
        self.assertEqual(response.status_code, 302)

    def test_label_authorized(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse_lazy("labels:index"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse_lazy("labels:create"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse_lazy("labels:update", kwargs={"pk": self.label.id})
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse_lazy("labels:delete", kwargs={"pk": self.label.id})
        )
        self.assertEqual(response.status_code, 200)
