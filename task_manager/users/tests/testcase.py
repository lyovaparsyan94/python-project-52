from django.test import Client, TestCase

from task_manager.users.models import User


class UserTestCase(TestCase):
    fixtures = ["test_users.json"]

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        
        self.user_count = User.objects.count()

        self.valid_data = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
        }

        self.update_data = {
            "first_name": "Updated",
            "last_name": "User",
            "username": "updateduser", 
            "password1": "updatedpass123",
            "password2": "updatedpass123",
        }
