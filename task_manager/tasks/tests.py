from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Labels
from task_manager.status.models import Statuses

from .filters import TaskFilter
from .models import Tasks

User = get_user_model()


class TaskTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            first_name="John",
            last_name='Doe',
            username="pork",
            password='111'
        )

        self.author_2 = User.objects.create_user(
            first_name="Sara",
            last_name='Man',
            username="girl",
            password='111'
        )

        self.maker = User.objects.create_user(
            first_name="J",
            last_name='Do',
            username="boyer",
            password='111'
        )

        self.maker_2 = User.objects.create_user(
            first_name="Jo",
            last_name='D',
            username="girly",
            password='111'
        )

        self.status = Statuses.objects.create(
            name='In progress',
        )

        self.status_2 = Statuses.objects.create(
            name='Вне работы',
        )

        self.label = Labels.objects.create(name='pog')
        self.label_2 = Labels.objects.create(name='gop')

        self.task = Tasks.objects.create(
            name="John",
            description="description",
            status=self.status,
            author=self.author,
            executor=self.maker,
        )

        self.task_2 = Tasks.objects.create(
            name="cat",
            description="descript",
            status=self.status,
            author=self.author_2,
            executor=self.maker,
        )

        self.task_3 = Tasks.objects.create(
            name="tac",
            description="desc",
            status=self.status_2,
            author=self.author_2,
            executor=self.maker_2,
        )

        labels_to_add = Labels.objects.filter(name__in=['pog', 'gop'])
        labels_to_add_2 = Labels.objects.filter(name__in=['gop'])
        self.task_2.labels.set(labels_to_add)
        self.task.labels.set(labels_to_add_2)

        self.queryset = Tasks.objects.all()

    def test_task_creation(self):

        self.assertEqual(self.task.name, "John")
        self.assertEqual(self.task.status.name, "In progress")
        self.assertEqual(self.task.author.username, "pork")
        self.assertEqual(self.task.executor.username, "boyer")

    def test_task_update(self):
        url = reverse('update_task', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.author)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        new_status = Statuses.objects.create(name='Updated')
        update_data = {
            'name': 'Updated',
            'description': 'Updated description',
            'executor': self.maker_2.id,
            'status': new_status.id,
            'labels': [self.label.id]
        }

        response = self.client.post(url, update_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.task.author, self.author)
        self.task.refresh_from_db()

        self.assertEqual(self.task.name, 'Updated')
        self.assertEqual(self.task.status.id, new_status.id)
        self.assertEqual(self.task.status.name, 'Updated')

    def test_task_delete(self):
        self.client.force_login(self.author)
        delete_url = reverse('delete_task', kwargs={'pk': self.task.pk})

        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))

        with self.assertRaises(Tasks.DoesNotExist):
            Tasks.objects.get(pk=self.task.pk)

    def test_filter(self):
        self.client.force_login(self.author)
        filtered = TaskFilter(
            data={'executor': self.maker.first_name},
            queryset=self.queryset
        )
        self.assertEqual(filtered.qs.count(), 3)
        self.assertEqual(filtered.qs.first().name, "John")

    def test_set_labels(self):

        self.assertIn(self.label, self.task_2.labels.all())
        self.assertIn(self.label_2, self.task.labels.all())

    def test_foreign_key_filtering(self):
        filtered = TaskFilter(
            data={'status': self.status_2},
            queryset=self.queryset
        ).qs
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first(), self.task_3)

    def test_many_to_many_filtering(self):
        result = TaskFilter({'labels': self.label}, self.queryset).qs
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), self.task_2)
