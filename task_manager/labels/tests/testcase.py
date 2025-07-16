from django.test import Client, TestCase

from task_manager.users.models import User

from task_manager.labels.models import Label


class LabelsTestCase(TestCase):
    fixtures = ["labels.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.label = Label.objects.get(pk=1)
        self.user = User.objects.get(pk=1)

        self.valid_data = {
            "name": "Test Label",
        }

        self.update_data = {
            "name": "Updated Label",
        }
