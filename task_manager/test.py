import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from task_manager.tasks.models import Task, Status, Label


class TestUser:
    @pytest.fixture(autouse=True)
    def setup(self, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            User = get_user_model()
            # Создаем тестовых пользователей
            User.objects.create_user(
                username='testuser1',
                password='testpass123',
                first_name='Test',
                last_name='User1',
                email='testuser1@example.com'
            )
            User.objects.create_user(
                username='testuser2',
                password='testpass123',
                first_name='Test',
                last_name='User2',
                email='testuser2@example.com'
            )
            User.objects.create_user(
                username='testuser3',
                password='testpass123',
                first_name='Test',
                last_name='User3',
                email='testuser3@example.com'
            )

    def test_load_users(self, transactional_db, django_user_model):
        users = django_user_model.objects.all()
        assert len(users) == 3

    def test_create_user(self, transactional_db, django_user_model):
        data_user = {
            "username": "testuser4",
            "first_name": "Test",
            "last_name": "User4",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        user = django_user_model.objects.create_user(**data_user)
        assert user.username == data_user["username"]
        assert user.first_name == data_user["first_name"]
        assert user.last_name == data_user["last_name"]

    def test_update_user(self, transactional_db, django_user_model):
        user = django_user_model.objects.get(username='testuser1')
        user.first_name = "Updated"
        user.save()
        updated_user = django_user_model.objects.get(username='testuser1')
        assert updated_user.first_name == "Updated"

    def test_delete_user(self, transactional_db, django_user_model):
        user = django_user_model.objects.get(username='testuser1')
        user.delete()
        assert not django_user_model.objects.filter(username='testuser1').exists()


class TestTask:
    @pytest.fixture(autouse=True)
    def setup(self, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            User = get_user_model()
            self.user = User.objects.create_user(
                username='taskuser',
                password='testpass123',
                first_name='Task',
                last_name='User',
                email='taskuser@example.com'
            )
            self.status = Status.objects.create(name='Test Status')
            self.label = Label.objects.create(name='Test Label')

    def test_create_task(self, transactional_db):
        task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            creator=self.user,
            executor=self.user
        )
        task.labels.add(self.label)
        assert task.name == 'Test Task'
        assert task.description == 'Test Description'
        assert task.status == self.status
        assert task.creator == self.user
        assert task.executor == self.user
        assert self.label in task.labels.all()

    def test_update_task(self, transactional_db):
        task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            creator=self.user,
            executor=self.user
        )
        task.name = 'Updated Task'
        task.save()
        updated_task = Task.objects.get(id=task.id)
        assert updated_task.name == 'Updated Task'

    def test_delete_task(self, transactional_db):
        task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            creator=self.user,
            executor=self.user
        )
        task.delete()
        assert not Task.objects.filter(name='Test Task').exists()


class TestStatus:
    @pytest.fixture(autouse=True)
    def setup(self, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            self.status = Status.objects.create(name='Test Status')

    def test_create_status(self, transactional_db):
        status = Status.objects.create(name='New Status')
        assert status.name == 'New Status'

    def test_update_status(self, transactional_db):
        self.status.name = 'Updated Status'
        self.status.save()
        updated_status = Status.objects.get(id=self.status.id)
        assert updated_status.name == 'Updated Status'

    def test_delete_status(self, transactional_db):
        self.status.delete()
        assert not Status.objects.filter(name='Test Status').exists()


class TestLabel:
    @pytest.fixture(autouse=True)
    def setup(self, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            self.label = Label.objects.create(name='Test Label')

    def test_create_label(self, transactional_db):
        label = Label.objects.create(name='New Label')
        assert label.name == 'New Label'

    def test_update_label(self, transactional_db):
        self.label.name = 'Updated Label'
        self.label.save()
        updated_label = Label.objects.get(id=self.label.id)
        assert updated_label.name == 'Updated Label'

    def test_delete_label(self, transactional_db):
        self.label.delete()
        assert not Label.objects.filter(name='Test Label').exists() 