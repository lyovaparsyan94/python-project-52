from task_manager.labels.forms import CreateLabelForm
from task_manager.labels.tests.testcase import LabelTestCase


class LabelTestForms(LabelTestCase):
    def test_valid_data(self):
        form = CreateLabelForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_missing_data(self):
        form = CreateLabelForm(data={"name": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_duplicate_name(self):
        form = CreateLabelForm(data={"name": self.label.name})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
