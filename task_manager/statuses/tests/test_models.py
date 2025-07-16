from django.test import TestCase

from task_manager.statuses.models import Status


class StatusModelTest(TestCase):
    def test_create_status(self):
        status = Status.objects.create(name='Test Status')
        self.assertEqual(status.name, 'Test Status')
        self.assertEqual(str(status), 'Test Status')

    def test_unique_name(self):
        Status.objects.create(name='Test Status')
        with self.assertRaises(Exception):
            Status.objects.create(name='Test Status')
