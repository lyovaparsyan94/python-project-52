from django.urls import reverse_lazy

from task_manager.statuses.tests.testcase import StatusTestCase


class StatusTestUrls(StatusTestCase):
    def test_status_unauthorized(self):
        response = self.client.get(reverse_lazy("statuses:index"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse_lazy("statuses:create"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse_lazy("statuses:update", kwargs={"pk": self.status.id})
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse_lazy("statuses:delete", kwargs={"pk": self.status.id})
        )
        self.assertEqual(response.status_code, 302)

    def test_status_authorized(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse_lazy("statuses:index"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse_lazy("statuses:create"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse_lazy("statuses:update", kwargs={"pk": self.status.id})
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse_lazy("statuses:delete", kwargs={"pk": self.status.id})
        )
        self.assertEqual(response.status_code, 200)
