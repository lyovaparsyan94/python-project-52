from django.urls import reverse_lazy

from task_manager.statuses.tests.testcase import StatusTestCase


class StatusesTestUrls(StatusTestCase):
    def test_status_unauthorized(self):
        response = self.client.get(reverse_lazy("statuses"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse_lazy("create_status"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse_lazy("update_status", kwargs={"pk": self.status.id})
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse_lazy("delete_status", kwargs={"pk": self.status.id})
        )
        self.assertEqual(response.status_code, 302)

    def test_status_authorized(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse_lazy("statuses"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse_lazy("create_status"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse_lazy("update_status", kwargs={"pk": self.status.id})
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse_lazy("delete_status", kwargs={"pk": self.status.id})
        )
        self.assertEqual(response.status_code, 200)
