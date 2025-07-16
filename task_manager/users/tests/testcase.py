from django.test import Client, TestCase

from task_manager.tasks.models import Tasks

from task_manager.users.models import Users


class UsersTestCase(TestCase):
    fixtures = ["users.json", "tasks.json", "statuses.json"]

    def setUp(self):
        self.client = Client()
        self.user1 = Users.objects.get(pk=1)
        self.user2 = Users.objects.get(pk=2)
        self.task = Tasks.objects.get(pk=1)

        self.valid_data = {
            "first_name": "Tom",
            "last_name": "Brady",
            "username": "TomBrady",
            "password": "Tom123",
            "confirm_password": "Tom123",
        }
