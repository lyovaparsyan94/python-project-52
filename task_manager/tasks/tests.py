from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .consts import TasksConst
from .models import Label, Status, Task

User = get_user_model()


class StatusTest(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        cache.clear()
        self.status_id = 7
        self.del_id = 14
        self.test_name = 'совсем зависло'
        self.exist_name = 'в работе'
        self.user_data = {'username': 'happylarry', 'password': '123'}
        self.status_data = {'name': self.test_name}
        self.exists_status_data = {'name': self.exist_name}

    def test_status_list(self):
        response = self.client.get(reverse('tasks:status_list'))
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.user_data)
        response = self.client.get(reverse('tasks:status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.context)
        items = response.context["items"]
        self.assertTrue(len(items) > 0)

    def test_create(self):
        response = self.client.post(
            reverse('tasks:create_status'),
            self.status_data,
            follow=True
        )

        self.assertRedirects(response, reverse('login'))
        self.client.login(**self.user_data)

        response = self.client.post(
            reverse('tasks:create_status'),
            self.status_data,
            follow=True
        )

        self.assertRedirects(response, reverse('tasks:status_list'))

        self.assertTrue(Status.objects.filter(name=self.test_name).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), TasksConst.status_succ_create)

        response = self.client.post(
            reverse('tasks:create_status'),
            self.exists_status_data,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TasksConst.status_exist)

    def test_update(self):

        url = reverse('tasks:update_status', kwargs={'pk': self.status_id})

        response = self.client.post(url, self.status_data, follow=True)

        self.assertRedirects(response, reverse('login'))
        self.client.login(**self.user_data)
        
        response = self.client.post(url, self.status_data, follow=True)

        self.assertRedirects(response, reverse('tasks:status_list'))

        status = Status.objects.filter(pk=self.status_id)[0]
        self.assertEqual(status.name, self.test_name)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), TasksConst.status_succ_update)

    def test_delete(self):

        url = reverse('tasks:delete_status', kwargs={'pk': self.del_id})
        url2 = reverse('tasks:delete_status', kwargs={'pk': self.status_id})

        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('login'))

        self.client.login(**self.user_data)

        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('tasks:status_list'))

        status = list(Status.objects.filter(pk=self.del_id))
        self.assertEqual(len(status), 0)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), TasksConst.status_succ_delete)

        response = self.client.post(url2, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TasksConst.status_used)


class LabelTest(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        cache.clear()
        self.label_id = 7
        self.label_no_delete = 15
        self.test_name = 'тестовая метка'
        self.exist_name = 'not use label'
        self.user_data = {'username': 'happylarry', 'password': '123'}
        self.label_data = {'name': self.test_name}
        self.exists_label_data = {'name': self.exist_name}

    def test_label_list(self):
        response = self.client.get(reverse('tasks:label_list'))
        self.assertEqual(response.status_code, 302)
        self.client.login(**self.user_data)
        response = self.client.get(reverse('tasks:label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.context)
        items = response.context["items"]
        self.assertTrue(len(items) > 0)

    def test_create(self):
        response = self.client.post(
            reverse('tasks:create_label'),
            self.label_data,
            follow=True
        )

        self.assertRedirects(response, reverse('login'))
        self.client.login(**self.user_data)

        response = self.client.post(
            reverse('tasks:create_label'),
            self.label_data,
            follow=True
        )

        self.assertRedirects(response, reverse('tasks:label_list'))

        self.assertTrue(Label.objects.filter(name=self.test_name).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), TasksConst.label_succ_create)

        response = self.client.post(
            reverse('tasks:create_label'),
            self.exists_label_data,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TasksConst.label_exist)

    def test_update(self):

        url = reverse('tasks:update_label', kwargs={'pk': self.label_id})

        response = self.client.post(url, self.label_data, follow=True)

        self.assertRedirects(response, reverse('login'))
        self.client.login(**self.user_data)
        
        response = self.client.post(url, self.label_data, follow=True)

        self.assertRedirects(response, reverse('tasks:label_list'))

        label = Label.objects.filter(pk=self.label_id)[0]
        self.assertEqual(label.name, self.test_name)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), TasksConst.label_succ_update)

    def test_delete(self):
        url = reverse('tasks:delete_label', kwargs={'pk': self.label_id})
        url2 = reverse(
            'tasks:delete_label',
            kwargs={'pk': self.label_no_delete})

        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('login'))

        self.client.login(**self.user_data)

        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('tasks:label_list'))

        label = list(Label.objects.filter(pk=self.label_id))
        self.assertEqual(len(label), 0)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), TasksConst.label_succ_delete)

        response = self.client.post(url2, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TasksConst.label_used)


class TaskTest(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        cache.clear()
        self.status_id = 7
        self. other_status_id = 10
        self.user_id = 9
        self.other_user_id = 9
        self.task_id = 2
        self.other_task_id = 3
        self.task_name = 'testname'
        self.test_descr = 'test description'
        self.test_name = 'совсем зависло'
        self.exist_name = 'в работе'
        self.user_data = {'username': 'happylarry', 'password': '123'}
        self.user_no_owner = {'username': 'harry777', 'password': '123'}
        self.status_data = {'name': self.test_name}
        self.exists_status_data = {'name': self.exist_name}

    def test_create(self):

        data = {
            'name': self.test_name,
            'description': self.test_descr,
            'executor': self.user_id,
            'status': self.status_id
        }

        response = self.client.post(reverse('tasks:create_task'),
                                    data,
                                    follow=True)

        self.assertRedirects(response, reverse('login'))

        self.client.login(**self.user_data)

        response = self.client.post(reverse('tasks:create_task'),
                                    data,
                                    follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TasksConst.task_succ_create)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), TasksConst.task_succ_create)

        self.assertTrue(Task.objects.filter(name=self.test_name).exists())

        response = self.client.post(reverse('tasks:create_task'),
                                    data,
                                    follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TasksConst.frm_unic_task)

    def test_index(self):
        response = self.client.get(reverse('tasks:task_list'), follow=True)

        self.assertRedirects(response, reverse('login'))

        self.client.login(**self.user_data)

        response = self.client.get(reverse('tasks:task_list'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TasksConst.task_term)

    def test_update(self):

        self.client.login(**self.user_data)

        data = {
            'name': self.test_name,
            'description': self.test_descr,
            'executor': self.other_user_id,
            'status': self.other_status_id
        }

        response = self.client.post(reverse('tasks:create_task'),
                                    data,
                                    follow=True)
        self.client.logout()

        data = {
            'name': self.test_name+'abc',
            'description': self.test_descr+'cde',
            'executor': self.other_user_id,
            'status': self.other_status_id
        }

        response = self.client.post(
            reverse('tasks:update_task', kwargs={'pk': self.task_id}),
            data,
            follow=True)

        self.assertRedirects(response, reverse('login'))

        self.client.login(**self.user_data)

        response = self.client.post(
            reverse('tasks:update_task', kwargs={'pk': self.task_id}),
            data,
            follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TasksConst.task_succ_update)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), TasksConst.task_succ_update)

        self.assertTrue(
            Task.objects.filter(name=self.test_name+'abc').exists())

        response = self.client.post(
            reverse('tasks:update_task', kwargs={'pk': self.other_task_id}),
            data,
            follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TasksConst.frm_unic_task)

    def test_detail(self):
        response = self.client.get(
            reverse('tasks:task_detail',
                    kwargs={'pk': self.task_id}), follow=True)

        self.assertRedirects(response, reverse('login'))

        self.client.login(**self.user_data)

        response = self.client.get(
            reverse('tasks:task_detail',
                    kwargs={'pk': self.task_id}), follow=True)

        task = Task.objects.filter(id=self.task_id).first()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task.name)

    def test_delete(self):
        url = reverse('tasks:delete_task', kwargs={'pk': self.task_id})

        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('login'))

        self.client.login(**self.user_data)

        data = {
            'name': self.test_name,
            'description': self.test_descr,
            'executor': self.other_user_id,
            'status': self.other_status_id
        }

        response = self.client.post(reverse('tasks:create_task'),
                                    data,
                                    follow=True)
        task_id = Task.objects.filter(name=self.test_name).first().id
        url = reverse('tasks:delete_task', kwargs={'pk': task_id})

        self.client.logout()

        self.client.login(**self.user_no_owner)

        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('tasks:task_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), TasksConst.task_error_delete)

        self.client.logout()

        self.client.login(**self.user_data)

        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('tasks:task_list'))

        tmp = list(Task.objects.filter(pk=task_id))
        self.assertEqual(len(tmp), 0)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(messages)
        self.assertEqual(str(messages[0]), TasksConst.task_succ_delete)
