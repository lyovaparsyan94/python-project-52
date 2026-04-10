from django.test import TestCase
from django.contrib.auth.models import User
from tasks.forms import TaskFilter
from tasks.models import Task
from task_manager.models import Status, Label


class TaskFilterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser')
        cls.status = Status.objects.create(name='Тест')
        cls.label = Label.objects.create(name='Тест')
        cls.task = Task.objects.create(
            name='Тестовая задача',
            status=cls.status,
            author=cls.user,
            executor=cls.user
        )
        cls.task.labels.add(cls.label)
    
    def test_filter_status(self):
        """Unit тест фильтра по статусу"""
        data = {'status': self.status.pk}
        f = TaskFilter(data, queryset=Task.objects.all())
        self.assertTrue(f.is_valid())
        self.assertEqual(f.qs.count(), 1)
        self.assertEqual(f.qs.first(), self.task)
    
    def test_filter_executor(self):
        """Unit тест фильтра по исполнителю"""
        data = {'executor': self.user.pk}
        f = TaskFilter(data, queryset=Task.objects.all())
        self.assertTrue(f.is_valid())
        self.assertEqual(f.qs.count(), 1)