from task_manager.statuses.forms import CreateStatusForm
from task_manager.statuses.tests.testcase import StatusTestCase


class StatusTestForms(StatusTestCase):
    def test_valid_data(self):
        form = CreateStatusForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_missing_data(self):
        form = CreateStatusForm(data={"name": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_duplicate_name(self):
        form = CreateStatusForm(data={"name": self.status.name})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
