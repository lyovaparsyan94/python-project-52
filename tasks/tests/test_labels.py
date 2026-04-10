from django.urls import reverse
from task_manager.models import Label
from tasks.models import Task


def test_task_create_with_labels(self):
    label = Label.objects.create(name='bug')
    self.client.login(username='test', password='pass123')

    data = {
        'name': 'Test task',
        'description': 'Test',
        'status': self.status.pk,
        'executor': self.user.pk,
        'labels': [label.pk]
    }

    self.client.post(reverse('tasks:create'), data)
    task = Task.objects.get(name='Test task')

    self.assertEqual(task.labels.count(), 1)
    self.assertIn(label, task.labels.all())
