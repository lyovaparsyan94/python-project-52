from django.utils import timezone

from task_manager.tasks.models import Task

from .testcase import TaskTestCase


class TaskModelTest(TaskTestCase):
    def test_task_creation(self):
        task = Task.objects.create(
            name='Test Task Creation',
            description='Test Description',
            status=self.status1,
            creator=self.user,
            executor=self.other_user
        )
        task.labels.add(self.label1, self.label2)
        
        self.assertEqual(task.name, 'Test Task Creation')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.status, self.status1)
        self.assertEqual(task.creator, self.user)
        self.assertEqual(task.executor, self.other_user)
        self.assertEqual(task.labels.count(), 2)
        self.assertEqual(str(task), 'Test Task Creation')
        
    def test_task_ordering(self):
        now = timezone.now()
        self.task1.created_at = now - timezone.timedelta(days=2)
        self.task1.save()

        self.task2.created_at = now - timezone.timedelta(days=1)
        self.task2.save()

        self.task3.created_at = now
        self.task3.save()

        tasks = Task.objects.all()
        self.assertEqual(tasks[0], self.task3)
        self.assertEqual(tasks[1], self.task2)
        self.assertEqual(tasks[2], self.task1)

