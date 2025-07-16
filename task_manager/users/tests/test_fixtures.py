from django.test import TestCase
from task_manager.users.models import User


class TestUserFixtures(TestCase):
    fixtures = ['test_users.json']

    def test_load_users(self):
        """Test that fixtures are loaded correctly."""
        users = User.objects.all()
        self.assertEqual(len(users), 3)
        
        # Проверяем конкретных пользователей
        john = User.objects.get(username='john_snow')
        self.assertEqual(john.first_name, 'John')
        self.assertEqual(john.last_name, 'Snow')
        
        daenerys = User.objects.get(username='daenerys_t')
        self.assertEqual(daenerys.first_name, 'Daenerys')
        
        arya = User.objects.get(username='arya_stark')
        self.assertEqual(arya.first_name, 'Arya') 