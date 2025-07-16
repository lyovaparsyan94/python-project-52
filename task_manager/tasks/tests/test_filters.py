from django.urls import reverse

from .testcase import TaskTestCase


class TaskFilterTest(TaskTestCase):
    def test_filter_by_status(self):
        response = self.client.get(
            reverse('tasks_list') + f'?status={self.status1.id}'
        )
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task3.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_by_executor(self):
        response = self.client.get(
            reverse('tasks_list') + f'?executor={self.other_user.id}'
        )
        self.assertContains(response, self.task2.name)
        self.assertNotContains(response, self.task1.name)
        self.assertNotContains(response, self.task3.name)

    def test_filter_by_labels(self):
        response = self.client.get(
            reverse('tasks_list') + f'?labels={self.label1.id}'
        )
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)

    def test_filter_self_tasks(self):
        response = self.client.get(
            reverse('tasks_list') + '?self_tasks=on'
        )
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)

    def test_combined_filters(self):
        response = self.client.get(
            reverse('tasks_list') + 
            f'?status={self.status1.id}&self_tasks=on'
        )
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)
