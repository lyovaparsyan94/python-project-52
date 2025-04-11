from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from yaml import CLoader, load

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()
path = (
    Path(__file__)
    .resolve()
    .parent.parent.joinpath("fixtures", "test_values.yaml")
)


class TaskTestCase(TestCase):
    fixtures = ["tasks.yaml"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(id=3)
        self.task1 = Task.objects.get(id=1)
        self.task2 = Task.objects.get(id=2)
        self.status = Status.objects.get(id=3)
        self.executor = User.objects.get(id=1)
        self.label = Label.objects.get(id=2)
        self.task_count = Task.objects.count()
        with path.open() as f:
            self.data = load(f, Loader=CLoader)
        self.valid_data = self.data.get("new_task")
        self.update_data = self.data.get("update_task")


class TaskViewsTest(TaskTestCase):
    def test_tasks_list(self):
        # user not authenticated
        response = self.client.get(reverse("tasks_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/tasks_list.html")
        self.assertEqual(Task.objects.count(), self.task_count)

    def test_tasks_filter(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("tasks_list"), {"status": self.status.id}
        )
        self.assertEqual(response.status_code, 200)
        tasks = set(response.context["tasks"])
        expected_tasks = set(Task.objects.filter(status=self.status))
        self.assertEqual(tasks, expected_tasks)

        response = self.client.get(
            reverse("tasks_list"), {"executor": self.executor.id}
        )
        self.assertEqual(response.status_code, 200)
        tasks = set(response.context["tasks"])
        expected_tasks = set(Task.objects.filter(executor=self.executor))
        self.assertEqual(tasks, expected_tasks)

        response = self.client.get(
            reverse("tasks_list"), {"labels": self.label.id}
        )
        self.assertEqual(response.status_code, 200)
        tasks = set(response.context["tasks"])
        expected_tasks = set(Task.objects.filter(labels=self.label))
        self.assertEqual(tasks, expected_tasks)

        response = self.client.get(reverse("tasks_list"), {"user_tasks": True})
        self.assertEqual(response.status_code, 200)
        tasks = set(response.context["tasks"])
        expected_tasks = set(Task.objects.filter(author=self.user))
        self.assertEqual(tasks, expected_tasks)

    def test_task_info(self):
        id = self.task1.id
        # user not authenticated
        response = self.client.get(reverse("task_info", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("task_info", args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_info.html")
        self.assertEqual(response.context["task"], self.task1)

        response = self.client.get(
            reverse("task_info", args=[self.task_count + 1])
        )
        self.assertEqual(response.status_code, 404)

    def test_create_task(self):
        # user not authenticated
        response = self.client.get(reverse("task_create"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        response = self.client.post(
            reverse("task_create"),
            self.valid_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("task_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")

        response = self.client.post(
            reverse("task_create"),
            self.valid_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), self.task_count + 1)
        self.assertEqual(
            Task.objects.filter(pk=self.task_count + 1)[0].name,
            self.valid_data.get("name"),
        )
        self.assertRedirects(response, reverse("tasks_list"))

    def test_update_task(self):
        # user not authenticated
        id = self.task1.id
        response = self.client.get(reverse("task_update", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        response = self.client.post(
            reverse("task_update", args=[id]), self.update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("task_update", args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")

        response = self.client.post(
            reverse("task_update", args=[id]), self.update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))
        self.assertEqual(
            Task.objects.get(id=id).description,
            self.update_data.get("description"),
        )

    def test_delete_task(self):
        # user not authenticated
        id = self.task2.id
        response = self.client.get(reverse("task_delete", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        response = self.client.post(reverse("task_delete", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse("task_delete", args=[id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete.html")

        response = self.client.post(reverse("task_delete", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))
        self.assertEqual(Task.objects.count(), self.task_count - 1)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=id)

        # user is authenticated, but task maded by another author
        id = self.task1.id
        response = self.client.get(reverse("task_delete", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))

        response = self.client.post(reverse("task_delete", args=[id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))
        self.assertEqual(Task.objects.count(), self.task_count - 1)
        self.assertEqual(
            Task.objects.get(id=id).description, self.task1.description
        )
