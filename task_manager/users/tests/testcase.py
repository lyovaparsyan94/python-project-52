from django.test import Client, TestCase

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class UserTestCase(TestCase):
    def setUp(self):
        user1 = {
            "first_name": "John",
            "last_name": "Snow",
            "username": "john_snow",
            "password": "Stark123",
        }

        user2 = {
            "first_name": "Daenerys",
            "last_name": "Targaryen",
            "username": "daenerys_t",
            "password": "Dracarys123",
        }

        user3 = {
            "first_name": "Arya",
            "last_name": "Stark",
            "username": "arya_stark",
            "password": "Arya123",
        }

        self.user1 = User.objects.create_user(**user1)
        self.user2 = User.objects.create_user(**user2)
        self.user3 = User.objects.create_user(**user3)

        status = {
            "name": "inwork",
            "created_at": "2023-08-11T17:04:28.819Z",
        }

        self.status = Status.objects.create(**status)

        task = {
            "name": "Defend the Wall",
            "description": "Coordinate the Night's Watch to "
            "defend Castle Black from wildlings.",
            "status": self.status,
            "author": self.user2,
            "executor": self.user1,
            "created_at": "2024-08-20T12:00:00Z",
        }

        self.client = Client()

        self.task = Task.objects.create(**task)

        self.valid_data = {
            "first_name": "Tom",
            "last_name": "Brady",
            "username": "TomBrady",
            "password1": "Tom123",
            "password2": "Tom123",
        }
