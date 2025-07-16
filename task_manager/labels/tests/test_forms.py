from django.test import TestCase

from task_manager.labels.forms import LabelForm


class LabelFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'name': 'New Label'}
        form = LabelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'name': ''}
        form = LabelForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
