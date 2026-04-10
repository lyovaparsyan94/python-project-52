from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.models import Label, Status
from tasks.models import Task

User = get_user_model()


class LabelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.status = Status.objects.create(name='Test Status')
        cls.user = User.objects.create_user(username='test', password='pass123')

    def setUp(self):
        self.client = Client()
        self.label = Label.objects.create(name='bug')

    def test_label_list(self):
        self.client.login(username='test', password='pass123')
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 200)

    def test_cannot_delete_if_used(self):
        task = Task.objects.create(
            name='test task',
            author=self.user,
            status=self.status,
            executor=self.user,
        )
        task.labels.add(self.label)

        print(f"Label tasks count: {self.label.tasks.count()}")
        print(f"Label tasks exists: {self.label.tasks.exists()}")
        print(f"Task labels: {task.labels.all()}")

        self.client.login(username='test', password='pass123')
        response = self.client.post(reverse('labels:delete', kwargs={'pk': self.label.pk}))

        print(f"After delete - Label exists: {Label.objects.filter(name='bug').exists()}")

        self.assertTrue(Label.objects.filter(name='bug').exists())