from django.test import TestCase

from task_manager.labels.models import Label
from task_manager.users.models import User


class LabelModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')

    def test_create_label(self):
        label = Label.objects.create(
            name='Test Label',
            creator=self.user
        )
        self.assertEqual(label.name, 'Test Label')
        self.assertEqual(label.creator, self.user)
        self.assertEqual(str(label), 'Test Label')

    def test_unique_name(self):
        Label.objects.create(name='Test Label', creator=self.user)
        with self.assertRaises(Exception):
            Label.objects.create(name='Test Label', creator=self.user)
