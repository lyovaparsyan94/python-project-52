# from django.test import TestCase

# Create your tests here.

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from task_manager.tasks.models import Status, Task, Label
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


class UserCRUDTestCase(TestCase):
    """Test user CRUD operations."""
    # fixtures = ['task_manager/tasks/fixtures/users.json']

    def setUp(self):
        self.client = Client()
        # Используем пользователей из фикстур
        # self.user1 = User.objects.get(username='testuser1')
        # self.user2 = User.objects.get(username='testuser2')
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        # Устанавливаем пароль, который можно использовать для входа
        # self.user1.set_password('testpass123')
        # self.user1.save()
        # self.user2.set_password('testpass123')
        # self.user2.save()

    def test_users_list(self):
        """Тест чтения списка пользователей."""
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser1')
        self.assertContains(response, 'testuser2')

    def test_user_registration(self):
        """Тест создания нового пользователя."""
        user_count = User.objects.count()
        registration_data = {
            'username': 'newuser',
            'password1': 'strong_test_pass123',
            'password2': 'strong_test_pass123',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com'
        }

        response = self.client.post(
            reverse('user_create'),
            data=registration_data,
            follow=True
        )

        # Проверяем успешный редирект на страницу входа
        self.assertRedirects(response, reverse('login'))

        # Проверяем, что пользователь был создан
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Проверяем сообщение об успешной регистрации
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно создан')

    def test_user_update(self):
        """Тест обновления профиля пользователя."""
        # Авторизуемся как testuser1
        self.client.login(username='testuser1', password='testpass123')

        # Данные для обновления
        update_data = {
            'username': 'updateduser1',
            'first_name': 'Updated',
            'last_name': 'User'
        }

        response = self.client.post(
            reverse('user_update', args=[self.user1.id]),
            data=update_data,
            follow=True
        )

        # Проверяем успешный редирект
        self.assertRedirects(response, reverse('users'))

        # Проверяем, что данные обновились
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'updateduser1')
        self.assertEqual(self.user1.first_name, 'Updated')

        # Проверяем сообщение
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно изменен')

    def test_user_update_permission(self):
        """Тест прав доступа: пользователь может редактировать
        только свой профиль."""
        # Авторизуемся как testuser1
        self.client.login(username='testuser1', password='testpass123')

        # Пытаемся обновить профиль testuser2
        update_data = {
            'username': 'hacked_user',
            'first_name': 'Hacked',
            'last_name': 'User'
        }

        response = self.client.post(
            reverse('user_update', args=[self.user2.id]),
            data=update_data,
            follow=True
        )

        # Проверяем редирект на главную страницу
        self.assertRedirects(response, reverse('users'))

        # Проверяем, что данные НЕ обновились
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.username, 'testuser2')

        # Проверяем сообщение об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'У вас нет прав для изменения другого пользователя'
        )

    def test_user_delete(self):
        """Тест удаления пользователя."""
        # Авторизуемся как testuser1
        login_successful = self.client.login(username='testuser1',
                                             password='testpass123')
        self.assertTrue(login_successful, "Не удалось войти в систему")

        # Проверяем, что пользователь действительно аутентифицирован
        response = self.client.get(reverse('users'))
        self.assertEqual(response.context['user'].username, 'testuser1')

        user_count = User.objects.count()

        response = self.client.post(
            reverse('user_delete', args=[self.user1.id]),
            follow=True
        )

        # Проверяем успешный редирект
        self.assertRedirects(response, reverse('users'))

        # Проверяем, что пользователь был удален
        self.assertEqual(User.objects.count(), user_count - 1)
        self.assertFalse(User.objects.filter(username='testuser1').exists())

        # Проверяем сообщение
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно удален')

    def test_user_delete_permission(self):
        """Тест прав доступа: пользователь может удалить
        только свой аккаунт."""
        # Авторизуемся как testuser1
        self.client.login(username='testuser1', password='testpass123')

        user_count = User.objects.count()

        # Пытаемся удалить testuser2
        response = self.client.post(
            reverse('user_delete', args=[self.user2.id]),
            follow=True
        )

        # Проверяем редирект
        # self.assertRedirects(response, reverse('login'))

        # Проверяем, что пользователь НЕ был удален
        self.assertEqual(User.objects.count(), user_count)
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())

        # Проверяем сообщение об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'У вас нет прав для удаления другого пользователя'
        )


class StatusCRUDTestCase(TestCase):
    """Test status CRUD operations."""
    fixtures = ['task_manager/tasks/fixtures/users.json',
                'task_manager/tasks/fixtures/statuses.json']

    def setUp(self):
        self.client = Client()
        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Login for CRUD operations
        self.client.login(username='testuser', password='testpass123')
        self.status1 = Status.objects.get(name='new')
        self.status2 = Status.objects.get(name='in progress')
        self.status3 = Status.objects.get(name='done')

    def test_status_list(self):
        """Тест чтения списка статусов."""
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'new')
        self.assertContains(response, 'in progress')
        self.assertContains(response, 'done')

    def test_status_create(self):
        """Тест создания нового статуса."""
        response = self.client.post(
            reverse('status_create'),
            data={'name': 'new_status'},
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(Status.objects.count(), 4)
        self.assertTrue(Status.objects.filter(name='new_status').exists())

    def test_status_update(self):
        """Тест обновления статуса."""
        response = self.client.post(
            reverse('status_update', args=[self.status1.id]),
            data={'name': 'updated_status'},
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, 'updated_status')

    def test_status_delete(self):
        """Тест удаления статуса."""
        response = self.client.post(
            reverse('status_delete', args=[self.status1.id]),
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(Status.objects.count(), 2)
        self.assertFalse(Status.objects.filter(id=self.status1.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно удален')

    def test_status_delete_permission(self):
        """Тест прав доступа: пользователь может удалить
        только свой статус."""
        # Logout first
        self.client.logout()

        response = self.client.post(
            reverse('status_delete', args=[self.status1.id]),
            follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Status.objects.count(), 3)
        self.assertTrue(Status.objects.filter(id=self.status1.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_status_update_permission(self):
        """Test that unauthorized users cannot update statuses."""
        # Logout first
        self.client.logout()

        # Try to update a status without being logged in
        update_data = {
            'name': 'unauthorized_update'
        }

        # Get initial status value to verify it doesn't change
        original_name = self.status1.name

        response = self.client.post(
            reverse('status_update', args=[self.status1.id]),
            data=update_data,
            follow=True
        )

        # Check redirect to login page
        self.assertRedirects(response, reverse('login'))
        # Verify status was not updated
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, original_name)

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')


class TaskCRUDTestCase(TestCase):
    """Test task CRUD operations."""
    fixtures = ['task_manager/tasks/fixtures/users.json',
                'task_manager/tasks/fixtures/statuses.json',
                'task_manager/tasks/fixtures/tasks.json',
                'task_manager/tasks/fixtures/labels.json']

    def setUp(self):
        self.client = Client()
        # Create test users
        self.user1 = User.objects.get(username='testuser1')
        self.user2 = User.objects.get(username='testuser2')
        self.user1.set_password('testpass123')
        self.user1.save()
        self.user2.set_password('testpass123')
        self.user2.save()
        # Read test labels from fixture
        self.label1 = Label.objects.get(name='label1')
        self.label2 = Label.objects.get(name='label2')
        # Get existing status from fixture
        self.status1 = Status.objects.get(name='new')
        # Create test tasks
        self.task1 = Task.objects.get(name='task1')
        self.task2 = Task.objects.get(name='task2')
        # Login as user1
        self.client.login(username='testuser1', password='testpass123')

    def test_task_list(self):
        """Чтение списка задач"""
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'task1')
        self.assertContains(response, 'task2')

    def test_create_task(self):
        # Создаём первого пользователя
        user1_data = {
            'username': 'testuser1',
            'first_name': 'user1',
            'last_name': 'userov1',
            'password1': 'stronGpassw1231',
            'password2': 'stronGpassw1231',
        }
        self.client.post(reverse('users:create'), user1_data)
        self.client.login(username='testuser1', password='stronGpassw1231')

        # Создаём второго пользователя
        user2_data = {
            'username': 'testuser2',
            'first_name': 'user2',
            'last_name': 'userov2',
            'password1': 'stronGpassw1232',
            'password2': 'stronGpassw1232',
        }
        self.client.post(reverse('users:create'), user2_data)

        # Создаём статус
        status_data = {"name": "status1"}
        self.client.post(reverse("statuses:create"), status_data)
        status = Status.objects.get(name=status_data["name"])

        # Создаём метку
        label_data = {"name": "label1"}
        self.client.post(reverse("labels:create"), label_data)
        label = Label.objects.get(name=label_data["name"])

        # Создаём задачу
        task_data = {
            "name": "task1",
            "description": "description1",
            "status": status.id,
            "executor": User.objects.get(username='testuser2').id,
            "labels": [label.id],
        }
        response = self.client.post(reverse("tasks:create"), task_data)
        self.assertRedirects(response, reverse("tasks:list"))
        task = Task.objects.get(name=task_data["name"])
        self.assertEqual(task.name, task_data["name"])
        self.assertEqual(task.description, task_data["description"])
        self.assertEqual(task.status.id, task_data["status"])
        self.assertEqual(task.executor.id, task_data["executor"])

    def test_update_task(self):
        # Создаём первого пользователя
        user1_data = {
            'username': 'testuser1',
            'first_name': 'user1',
            'last_name': 'userov1',
            'password1': 'stronGpassw1231',
            'password2': 'stronGpassw1231',
        }
        self.client.post(reverse('users:create'), user1_data)
        self.client.login(username='testuser1', password='stronGpassw1231')

        # Создаём второго пользователя
        user2_data = {
            'username': 'testuser2',
            'first_name': 'user2',
            'last_name': 'userov2',
            'password1': 'stronGpassw1232',
            'password2': 'stronGpassw1232',
        }
        self.client.post(reverse('users:create'), user2_data)

        # Создаём третьего пользователя
        user3_data = {
            'username': 'testuser3',
            'first_name': 'user3',
            'last_name': 'userov3',
            'password1': 'stronGpassw1233',
            'password2': 'stronGpassw1233',
        }
        self.client.post(reverse('users:create'), user3_data)

        # Создаём статус
        status_data = {"name": "status1"}
        self.client.post(reverse("statuses:create"), status_data)
        status = Status.objects.get(name=status_data["name"])

        # Создаём метку
        label_data = {"name": "label1"}
        self.client.post(reverse("labels:create"), label_data)
        label = Label.objects.get(name=label_data["name"])

        # Создаём задачу
        task_data = {
            "name": "task1",
            "description": "description1",
            "status": status.id,
            "executor": User.objects.get(username='testuser2').id,
            "labels": [label.id],
        }
        self.client.post(reverse("tasks:create"), task_data)
        task = Task.objects.get(name=task_data["name"])

        # Обновляем задачу
        task_update_data = {
            "name": "task1_updated",
            "description": "description1_updated",
            "status": status.id,
            "executor": User.objects.get(username='testuser3').id,
            "labels": [label.id],
        }
        response = self.client.post(
            reverse("tasks:update", args=[task.id]), task_update_data
        )
        self.assertRedirects(response, reverse("tasks:list"))
        task.refresh_from_db()
        self.assertEqual(task.name, task_update_data["name"])
        self.assertEqual(task.description, task_update_data["description"])

    def test_delete_task(self):
        # Создаём первого пользователя
        user1_data = {
            'username': 'testuser1',
            'first_name': 'user1',
            'last_name': 'userov1',
            'password1': 'stronGpassw1231',
            'password2': 'stronGpassw1231',
        }
        self.client.post(reverse('users:create'), user1_data)
        self.client.login(username='testuser1', password='stronGpassw1231')

        # Создаём второго пользователя
        user2_data = {
            'username': 'testuser2',
            'first_name': 'user2',
            'last_name': 'userov2',
            'password1': 'stronGpassw1232',
            'password2': 'stronGpassw1232',
        }
        self.client.post(reverse('users:create'), user2_data)

        # Создаём статус
        status_data = {"name": "status1"}
        self.client.post(reverse("statuses:create"), status_data)
        status = Status.objects.get(name=status_data["name"])

        # Создаём метку
        label_data = {"name": "label1"}
        self.client.post(reverse("labels:create"), label_data)
        label = Label.objects.get(name=label_data["name"])

        # Создаём задачу
        task_data = {
            "name": "task1",
            "description": "description1",
            "status": status.id,
            "executor": User.objects.get(username='testuser2').id,
            "labels": [label.id],
        }
        self.client.post(reverse("tasks:create"), task_data)
        task = Task.objects.get(name=task_data["name"])

        # Удаляем задачу
        response = self.client.post(reverse("tasks:delete", args=[task.id]))
        self.assertRedirects(response, reverse("tasks:list"))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(name=task_data["name"])

    def test_task_permissions(self):
        # Создаём первого пользователя
        user1_data = {
            'username': 'testuser1',
            'first_name': 'user1',
            'last_name': 'userov1',
            'password1': 'stronGpassw1231',
            'password2': 'stronGpassw1231',
        }
        self.client.post(reverse('users:create'), user1_data)
        self.client.login(username='testuser1', password='stronGpassw1231')

        # Создаём второго пользователя
        user2_data = {
            'username': 'testuser2',
            'first_name': 'user2',
            'last_name': 'userov2',
            'password1': 'stronGpassw1232',
            'password2': 'stronGpassw1232',
        }
        self.client.post(reverse('users:create'), user2_data)

        # Создаём статус
        status_data = {"name": "status1"}
        self.client.post(reverse("statuses:create"), status_data)
        status = Status.objects.get(name=status_data["name"])

        # Создаём метку
        label_data = {"name": "label1"}
        self.client.post(reverse("labels:create"), label_data)
        label = Label.objects.get(name=label_data["name"])

        # Создаём задачу от имени первого пользователя
        task_data = {
            "name": "task1",
            "description": "description1",
            "status": status.id,
            "executor": User.objects.get(username='testuser2').id,
            "labels": [label.id],
        }
        self.client.post(reverse("tasks:create"), task_data)
        task = Task.objects.get(name=task_data["name"])

        # Логинимся как второй пользователь
        self.client.logout()
        self.client.login(username='testuser2', password='stronGpassw1232')

        # Пытаемся удалить чужую задачу
        response = self.client.post(reverse("tasks:delete", args=[task.id]))
        self.assertRedirects(response, reverse("tasks:list"))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            'Задачу может удалить только её автор',
            str(messages[0])
        )
        # Проверяем, что задача всё ещё существует
        self.assertTrue(Task.objects.filter(name=task_data["name"]).exists())


class LabelCRUDTestCase(TestCase):
    """Test label CRUD operations."""
    fixtures = ['task_manager/tasks/fixtures/users.json',
                'task_manager/tasks/fixtures/statuses.json',
                'task_manager/tasks/fixtures/labels.json',
                'task_manager/tasks/fixtures/tasks.json']

    def setUp(self):
        self.client = Client()
        # Create test users
        self.user1 = User.objects.get(username='testuser1')
        self.user1.set_password('testpass123')
        self.user1.save()
        # Read test labels from fixture
        self.label1 = Label.objects.get(name='label1')
        self.label2 = Label.objects.get(name='label2')
        # Get existing status from fixture
        self.status1 = Status.objects.get(name='new')
        # Create test tasks
        self.task1 = Task.objects.get(name='task1')
        self.task2 = Task.objects.get(name='task2')
        # Login as user1
        self.client.login(username='testuser1', password='testpass123')

    def test_label_list(self):
        """Read label list"""
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'label1')
        self.assertContains(response, 'label2')

    def test_label_create(self):
        """Test new label creation."""
        response = self.client.post(
            reverse('label_create'),
            data={'name': 'new_label'},
            follow=True
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertEqual(Label.objects.count(), 3)
        self.assertTrue(Label.objects.filter(name='new_label').exists())

    def test_label_update(self):
        """Test label update."""
        response = self.client.post(
            reverse('label_update', args=[self.label1.id]),
            data={'name': 'updated_label'},
            follow=True
        )
        self.assertRedirects(response, reverse('labels'))
        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, 'updated_label')

    def test_label_delete_unauthenticated(self):
        """Тест попытки удаления label неавторизованным пользователем."""
        self.client.logout()
        response = self.client.post(
            reverse('label_delete', args=[self.label2.id]),
            follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(Task.objects.filter(id=self.label2.id).exists())
        messages = list(response.context['messages'])
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )

    def test_label_delete_authenticated(self):
        """Тест удаления label."""
        response = self.client.post(
            reverse('label_delete', args=[self.label2.id]),
            follow=True
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertEqual(Label.objects.count(), 1)
        self.assertFalse(Label.objects.filter(id=self.label2.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно удалена')

    def test_label_delete_with_tasks(self):
        """Test that label cannot be deleted if it's used in tasks."""
        # Associate label1 with task1
        self.task1.labels.add(self.label1)

        response = self.client.post(
            reverse('label_delete', args=[self.label1.id]),
            follow=True
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(id=self.label1.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Невозможно удалить метку, потому что она используется'
        )
