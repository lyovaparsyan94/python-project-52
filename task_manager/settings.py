import os
import sys
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path
from django.utils.translation import gettext as _

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, BASE_DIR)

APP_DIR = Path(__file__).resolve().parent 

print(f"Absolute path to settings.py: {os.path.abspath(__file__)}")
print(f"Computed BASE_DIR: {BASE_DIR}")

load_dotenv(os.path.join(BASE_DIR, '.env'))

TESTING = 'test' in sys.argv

if TESTING:
    SECRET_KEY = 'django-insecure-test-secret-key-for-ci'
else:
    SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-for-dev')
    
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'webserver',
    'hexlet-code-d230.onrender.com',
    'localhost',
    '127.0.0.1',
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = [
    'task_manager.users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'whitenoise.runserver_nostatic',
    'django_bootstrap5',
    'task_manager.statuses',
    'task_manager.labels',
    'task_manager.tasks', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404',
]

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
]

LOCALE_PATHS = [os.path.join(APP_DIR, 'locale')]

USE_I18N = True
ROOT_URLCONF = 'task_manager.urls' 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(APP_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'task_manager.users.context_processors.language_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'task_manager.wsgi.application'

if os.getenv('CI') or DEBUG or TESTING or 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3'),
            conn_max_age=600,
            engine='django.db.backends.postgresql'
        )
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru' if not TESTING else 'en'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BOOTSTRAP5 = {
    'theme_url': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
}

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

ROLLBAR_ACCESS_TOKEN = os.getenv('ROLLBAR_ACCESS_TOKEN')
if ROLLBAR_ACCESS_TOKEN and not DEBUG and not TESTING:
    ROLLBAR = {
        'access_token': ROLLBAR_ACCESS_TOKEN,
        'environment': os.getenv('ROLLBAR_ENVIRONMENT', 'production'),
        'root': BASE_DIR,
    }
    MIDDLEWARE.append('rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404')

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'rollbar': {
                'class': 'rollbar.logger.RollbarHandler',
                'access_token': ROLLBAR_ACCESS_TOKEN,
                'environment': os.getenv('ROLLBAR_ENVIRONMENT', 'production'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['rollbar'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
else:
    LOGGING = {}

if TESTING:
    print("\n=== TESTING MODE ===")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"sys.path: {sys.path}")
    print(f"INSTALLED_APPS: {INSTALLED_APPS}\n")
    LANGUAGE_CODE = 'en'
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    WHITENOISE_AUTOREFRESH = True

print("\n" + "="*50)
print(f"LOCALE_PATHS: {LOCALE_PATHS}")
