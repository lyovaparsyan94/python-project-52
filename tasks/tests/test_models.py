from django.test import TestCase
from django.contrib.auth import get_user_model
from tasks.models import Task, Status

User = get_user_model()


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        cls.status = Status.objects.create(name='New')
        cls.task = Task.objects.create(
            name='Тестовая задача',
            description='Описание задачи',
            author=cls.user,
            status=cls.status,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.task), 'Тестовая задача')

    def test_task_author_default(self):
        self.assertEqual(self.task.author, self.user)

    def test_task_verbose_name_plural(self):
        self.assertEqual(
            Task._meta.verbose_name_plural,
            'Задачи'
        )
