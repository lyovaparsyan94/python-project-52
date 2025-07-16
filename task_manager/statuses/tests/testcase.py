from django.test import Client, TestCase

from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusTestCase(TestCase):
    fixtures = ["test_statuses.json", "test_users.json"]

    def setUp(self):
        self.client = Client()
        self.status1 = Status.objects.get(pk=1)
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

        self.valid_data = {
            "name": "Test Status",
        }

        self.update_data = {
            "name": "Updated Status",
        }
