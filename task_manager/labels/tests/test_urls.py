from django.urls import reverse_lazy

from task_manager.labels.tests.testcase import LabelsTestCase


class LabelsTestUrls(LabelsTestCase):
    def test_label_unauthorized(self):
        response = self.client.get(reverse_lazy("labels"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse_lazy("create_label"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse_lazy("update_label", kwargs={"pk": self.label.id})
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse_lazy("delete_label", kwargs={"pk": self.label.id})
        )
        self.assertEqual(response.status_code, 302)

    def test_label_authorized(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse_lazy("labels"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse_lazy("create_label"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse_lazy("update_label", kwargs={"pk": self.label.id})
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse_lazy("delete_label", kwargs={"pk": self.label.id})
        )
        self.assertEqual(response.status_code, 200)
