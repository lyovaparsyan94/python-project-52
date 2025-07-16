from task_manager.statuses.models import Statuses
from task_manager.statuses.tests.testcase import StatusTestCase


class StatusesTestModel(StatusTestCase):
    def test_status_creation(self):
        initial_count = Statuses.objects.count()
        Statuses.objects.create(**self.valid_data)
        self.assertEqual(Statuses.objects.count(), initial_count + 1)

    def test_status_duplicate_name(self):
        with self.assertRaises(Exception):
            Statuses.objects.create({"name": self.label.name})

    def test_status_missing_name(self):
        with self.assertRaises(Exception):
            Statuses.objects.create({"name": ""})
