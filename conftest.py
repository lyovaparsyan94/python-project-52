import pytest
from django.core.management import call_command


@pytest.fixture(autouse=True)
def load_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'task_manager/users/fixtures/users.json') 