from task_manager.labels.models import Labels
from task_manager.labels.tests.testcase import LabelsTestCase


class LabelsTestModel(LabelsTestCase):
    def test_label_creation(self):
        initial_count = Labels.objects.count()
        Labels.objects.create(**self.valid_data)
        self.assertEqual(Labels.objects.count(), initial_count + 1)

    def test_label_duplicate_name(self):
        with self.assertRaises(Exception):
            Labels.objects.create({"name": self.label.name})

    def test_label_missing_name(self):
        with self.assertRaises(Exception):
            Labels.objects.create({"name": ""})
