import pytest
import os
import django
from django.conf import settings
from django.test.utils import get_runner


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_URL', '').split('/')[-1],
        'USER': 'hexlet',
        'PASSWORD': 'hexlet',
        'HOST': 'db',
        'PORT': '5432',
    }


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass 