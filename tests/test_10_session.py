from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUser(TestCase):
    fixtures = ['users.json']

    def test_load_users(self, django_user_model):
        users = django_user_model.objects.all()
        assert len(users) == 3 