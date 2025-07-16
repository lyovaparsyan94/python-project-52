from django.test import TestCase

from task_manager.statuses.forms import StatusForm


class StatusFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'name': 'New Status'}
        form = StatusForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'name': ''}
        form = StatusForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
