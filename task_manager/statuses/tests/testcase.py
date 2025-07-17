from django.test import Client, TestCase

from task_manager.users.models import Users

from task_manager.statuses.models import Statuses


class StatusTestCase(TestCase):
    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.status = Statuses.objects.get(pk=1)
        self.user = Users.objects.get(pk=1)

        self.valid_data = {
            "name": "Test Status",
        }

        self.update_data = {
            "name": "Updated Status",
        }
