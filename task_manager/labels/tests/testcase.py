from django.test import Client, TestCase

from task_manager.labels.models import Label
from task_manager.users.models import User


class LabelTestCase(TestCase):
    fixtures = ["test_labels.json", "test_users.json"]

    def setUp(self):
        self.client = Client()
        self.label1 = Label.objects.get(pk=1)
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        
        self.label_count = Label.objects.count()

        self.valid_data = {
            "name": "Test Label",
        }

        self.update_data = {
            "name": "Updated Label",
        }
