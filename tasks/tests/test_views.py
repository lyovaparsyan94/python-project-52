from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from tasks.models import Task, Status
from django.test.utils import override_settings

User = get_user_model()


class TaskViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        cls.user2 = User.objects.create_user(
            username='otheruser',
            password='pass123'
        )
        cls.status = Status.objects.create(name='New')
        
        cls.task = Task.objects.create(
            name='Задача для тестов',
            description='Описание',
            author=cls.user,
            status=cls.status,
            executor=cls.user
        )

    def test_tasks_list_view(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('tasks:tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задачи')
        self.assertContains(response, self.task.name)

    def test_task_create_view(self):
        self.client.login(username='testuser', password='pass123')
        data = {
            'name': 'Новая задача',
            'description': 'Описание новой задачи',
            'status': self.status.pk,
            'executor': self.user.pk,
        }
        response = self.client.post(reverse('tasks:create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:tasks'))
        self.assertTrue(Task.objects.filter(name='Новая задача').exists())

    def test_task_update_view_own(self):
        """Пользователь может редактировать свою задачу."""
        self.client.login(username='testuser', password='pass123')
        data = {
            'name': 'Обновлённая задача',
            'description': 'Обновлённое описание',
            'status': self.status.pk,
            'executor': self.user.pk,
        }
        response = self.client.post(
            reverse('tasks:update', kwargs={'pk': self.task.pk}),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Обновлённая задача')

    def test_task_update_view_not_owner(self):
        """Не‑автор не может редактировать задачу."""
        self.client.login(username='otheruser', password='pass123')
        data = {
            'name': 'Взломанная задача',
            'description': 'Нет',
            'status': self.status.pk,
            'executor': self.user.pk,
        }
        response = self.client.post(
            reverse('tasks:update', kwargs={'pk': self.task.pk}),
            data,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks:tasks'))
        
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertIn('Задачу может редактировать только её автор', str(messages_list[0]))


    def test_task_delete_view_own(self):
        """Пользователь может удалить свою задачу."""
        self.client.login(username='testuser', password='pass123')
        task = Task.objects.create(
            name='Удаляемая задача',
            author=self.user,
            status=self.status,
            executor=self.user
        )
        response = self.client.post(
            reverse('tasks:delete', kwargs={'pk': task.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name='Удаляемая задача').exists())

    def test_task_delete_view_not_owner(self):
        """Не‑автор не может удалить задачу."""
        self.client.login(username='otheruser', password='pass123')
        
        print("=== DEBUG ===")
        print("self.task:", self.task.pk, self.task.author.username)
        print("Logged in as:", self.client.session['_auth_user_id'])
        
        response = self.client.post(
            reverse('tasks:delete', kwargs={'pk': self.task.pk}),
            follow=True
        )
        
        print("Response status_code:", response.status_code)
        print("Redirected to:", response.redirect_chain)
        print("Messages:", list(response.context['messages']) if response.context else "NO CONTEXT!")
        
        self.assertRedirects(response, reverse('tasks:tasks'))
        
        messages_list = list(response.context['messages'])
        print("Final messages count:", len(messages_list))
        
        self.assertEqual(len(messages_list), 1)
