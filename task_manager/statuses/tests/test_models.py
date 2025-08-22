from task_manager.statuses.models import Status
from task_manager.statuses.tests.testcase import StatusTestCase


class StatusTestModel(StatusTestCase):
    def test_status_creation(self):
        initial_count = Status.objects.count()
        Status.objects.create(**self.valid_data)
        self.assertEqual(Status.objects.count(), initial_count + 1)

    def test_status_duplicate_name(self):
        with self.assertRaises(Exception):
            Status.objects.create({"name": self.label.name})

    def test_status_missing_name(self):
        with self.assertRaises(Exception):
            Status.objects.create({"name": ""})
