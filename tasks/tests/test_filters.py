from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task
from task_manager.models import Status, Label

class TaskFilterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаём пользователей
        cls.user1 = User.objects.create_user(username='user1', password='pass')
        cls.user2 = User.objects.create_user(username='user2', password='pass')
        
        # Создаём статусы
        cls.status_new = Status.objects.create(name='Новая')
        cls.status_done = Status.objects.create(name='Выполнена')
        
        # Создаём метки
        cls.label_frontend = Label.objects.create(name='Frontend')
        cls.label_backend = Label.objects.create(name='Backend')
        
        # Создаём задачи
        cls.task1 = Task.objects.create(
            name='Фронтенд задача',
            status=cls.status_new,
            author=cls.user1,
            executor=cls.user1
        )
        cls.task1.labels.add(cls.label_frontend)
        
        cls.task2 = Task.objects.create(
            name='Бэкенд задача',
            status=cls.status_done,
            author=cls.user2,
            executor=cls.user2
        )
        cls.task2.labels.add(cls.label_backend)
    
    def test_filter_status(self):
        """Фильтр по статусу"""
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('tasks:tasks'), {'status': self.status_new.pk})
        
        self.assertContains(response, 'Фронтенд задача')
        self.assertNotContains(response, 'Бэкенд задача')
    
    def test_filter_executor(self):
        """Фильтр по исполнителю"""
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('tasks:tasks'), {'executor': self.user1.pk})
        
        self.assertContains(response, 'Фронтенд задача')
        self.assertNotContains(response, 'Бэкенд задача')
    
    def test_filter_labels(self):
        """Фильтр по меткам"""
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('tasks:tasks'), {'labels': self.label_frontend.pk})
        
        self.assertContains(response, 'Фронтенд задача')
        self.assertNotContains(response, 'Бэкенд задача')
    
    def test_filter_is_owner(self):
        """Фильтр 'Только свои задачи'"""
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('tasks:tasks'), {'is_owner': 'on'})
        
        self.assertContains(response, 'Фронтенд задача')
        self.assertNotContains(response, 'Бэкенд задача')
    
    def test_filter_multiple(self):
        """Комбинированная фильтрация"""
        self.client.login(username='user1', password='pass')
        response = self.client.get(
            reverse('tasks:tasks'), 
            {
                'status': self.status_new.pk,
                'executor': self.user1.pk,
                'labels': self.label_frontend.pk
            }
        )
        
        self.assertContains(response, 'Фронтенд задача')
        self.assertNotContains(response, 'Бэкенд задача')
    
    def test_filter_reset(self):
        """Сброс фильтров"""
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('tasks:tasks'))
        
        self.assertContains(response, 'Фронтенд задача')