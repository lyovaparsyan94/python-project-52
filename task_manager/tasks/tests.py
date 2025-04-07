from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from task_manager.tasks.models import Tasks
from task_manager.statuses.models import Statuses
from task_manager.tasks.filter import TaskFilter
from task_manager.labels.models import Labels

class TasksTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Создание тестового пользователя, исполнителя и статуса"""
        cls.user = get_user_model().objects.create(
            username="volkovor777228",
            first_name="Lev",
            last_name="Smith",
        )
        cls.user.set_password("1234")
        cls.user.save()

        cls.executor = get_user_model().objects.create(
            username="Slava",
            first_name="Slava",
            last_name="Petrov",
        )
        cls.executor.set_password("1234")
        cls.executor.save()

        cls.status = Statuses.objects.create(name="oka")
        cls.status2 = Statuses.objects.create(name='Slava')
    def setUp(self):
        """Логиним пользователя перед каждым тестом"""
        login_successful = self.client.login(username="volkovor777228", password="1234")
        self.assertTrue(login_successful, "Не удалось залогинить пользователя!")


    def test_create_task(self):
        """Проверка создания задачи"""
        data_task = {
            "name": "enjoy",
            "description": "gsgsd",
            "status": self.status.pk,  
            "executor": self.executor.pk,
        }
        response = self.client.post(reverse("tasks:create"), data_task)

        self.assertRedirects(response, reverse("tasks:list"))

        task = Tasks.objects.get(name=data_task["name"])
        self.assertEqual(task.name, data_task["name"])
        self.assertEqual(task.description, data_task["description"])
        self.assertEqual(task.status.pk, data_task["status"])
        self.assertEqual(task.executor.pk, data_task["executor"])

    def test_update_task(self):
        """Проверка обновления задачи"""
        data_task = {
            "name": "enjoy",
            "description": "gsgsd",
            "status": self.status.pk,
            "executor": self.executor.pk,
        }
        self.client.post(reverse("tasks:create"), data_task)

        task = Tasks.objects.get(name=data_task["name"])
        self.assertEqual(task.name, data_task["name"])

        data_task_update = {
            "name": "enjoy_updated",
            "description": "new description",
            "status": self.status.pk,
            "executor": self.executor.pk,
        }
        response = self.client.post(
            reverse("tasks:update", args=[task.pk]), data_task_update
        )

        self.assertRedirects(response, reverse("tasks:list"))

        updated_task = Tasks.objects.get(pk=task.pk)
        self.assertEqual(updated_task.name, data_task_update["name"])
        self.assertEqual(updated_task.description, data_task_update["description"])

    def test_delete_task(self):
        """Проверка удаления задачи"""
        data_task = {
            "name": "enjoy",
            "description": "gsgsd",
            "status": self.status.pk,
            "executor": self.executor.pk,
        }
        self.client.post(reverse("tasks:create"), data_task)
        task = Tasks.objects.get(name=data_task["name"])

        self.assertEqual(task.name, data_task["name"])

        response = self.client.post(reverse("tasks:delete", args=[task.pk]))

        self.assertRedirects(response, reverse("tasks:list"))

        with self.assertRaises(ObjectDoesNotExist):
            Tasks.objects.get(name=data_task["name"])

    def test_filter_tasks_by_status(self):
        """Проверка фильтрации задач по статусу"""
        task1 = Tasks.objects.create(
            name="Task 1",
            description="Description 1",
            status=self.status,
            creator=self.user,
            executor=self.executor,
        )
        task2 = Tasks.objects.create(
            name="Task 2",
            description="Description 2",
            status=self.status,
            creator=self.user,
            executor=None,
        )
        task3 = Tasks.objects.create(
            name="Task 3",
            description="Description 3",
            status=self.status2,
            creator=self.user,
            executor=None,
        )

        response = self.client.get(reverse("tasks:list"), {'status': self.status.pk})
        self.assertContains(response, task1.name)
        self.assertContains(response, task2.name)
        self.assertNotContains(response, task3.name)


    def test_filter_tasks_by_executor(self):
        """Проверка фильтрации задач по исполнителю"""
        task1 = Tasks.objects.create(
            name="Task 1",
            description="Description 1",
            status=self.status,
            creator=self.user,
            executor=self.executor,
        )
        task2 = Tasks.objects.create(
            name="Task 2",
            description="Description 2",
            status=self.status,
            creator=self.user,
            executor=self.user,
        )

        response = self.client.get(reverse("tasks:list"), {'executor': self.executor.pk})
        self.assertContains(response, task1.name)
        self.assertNotContains(response, task2.name)

    def test_filter_tasks_by_label(self):
        """Проверка фильтрации задач по метке"""
        label = Labels.objects.create(name="Important")
        task1 = Tasks.objects.create(
            name="Task 1",
            description="Description 1",
            status=self.status,
            creator=self.user,
            executor=self.executor,
        )
        task1.label.add(label)

        task2 = Tasks.objects.create(
            name="Task 2",
            description="Description 2",
            status=self.status,
            creator=self.user,
            executor=self.user,
        )

        response = self.client.get(reverse("tasks:list"), {'task_label': label.pk})
        self.assertContains(response, task1.name)
        self.assertNotContains(response, task2.name)

    def test_list_tasks_view(self):
        """Проверка отображения списка задач"""
        task1 = Tasks.objects.create(
            name="Task 1",
            description="Description 1",
            status=self.status,
            creator=self.user,
            executor=self.executor,
        )
        task2 = Tasks.objects.create(
            name="Task 2",
            description="Description 2",
            status=self.status,
            creator=self.user,
            executor=None,
        )

        response = self.client.get(reverse("tasks:list"))
        self.assertContains(response, task1.name)
        self.assertContains(response, task2.name)
