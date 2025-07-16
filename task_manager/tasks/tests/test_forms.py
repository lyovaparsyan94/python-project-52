
from task_manager.tasks.forms import TaskForm

from .testcase import TaskTestCase


class TaskFormTest(TaskTestCase):
    def test_valid_form(self):
        form_data = {
            'name': 'Valid Task',
            'description': 'Valid description',
            'status': self.status1.pk,
            'executor': self.other_user.pk,
            'labels': [self.label1.pk, self.label2.pk]
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_name(self):
        form_data = {
            'name': '',
            'description': 'Missing name',
            'status': self.status1.pk
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_invalid_form_missing_status(self):
        form_data = {
            'name': 'No Status',
            'description': 'Missing status',
            'status': None
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('status', form.errors)
