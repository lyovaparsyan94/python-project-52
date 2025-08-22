from task_manager.labels.models import Label
from task_manager.labels.tests.testcase import LabelTestCase


class LabelTestModel(LabelTestCase):
    def test_label_creation(self):
        initial_count = Label.objects.count()
        Label.objects.create(**self.valid_data)
        self.assertEqual(Label.objects.count(), initial_count + 1)

    def test_label_duplicate_name(self):
        with self.assertRaises(Exception):
            Label.objects.create({"name": self.label.name})

    def test_label_missing_name(self):
        with self.assertRaises(Exception):
            Label.objects.create({"name": ""})
