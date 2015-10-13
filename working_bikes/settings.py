import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_NAME = 'WORKING_BIKES'
PROJECT_VARIABLE_PATTERN = '_'.join((PROJECT_NAME, '{}'))

SECRET_KEY = os.getenv(PROJECT_VARIABLE_PATTERN.format('SECRET_KEY'))

DEBUG = os.getenv(PROJECT_VARIABLE_PATTERN.format('DEBUG'), False) == 'TRUE'
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = os.getenv(PROJECT_VARIABLE_PATTERN.format('ALLOWED_HOSTS'), '*').split(',')

ADMINS = (
    ('Dane Hillard', 'github@danehillard.com'),
)

MANAGERS = ADMINS

ADMIN_URL = os.getenv(PROJECT_VARIABLE_PATTERN.format('ADMIN_URL'), 'r^admin/')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LOGIN_REDIRECT_URL = '/volunteer/profile/'
LOGIN_URL = '/volunteer/login/'
LOGOUT_URL = '/volunteer/logout/'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'volunteer',
    'explorer',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'working_bikes.urls'

WSGI_APPLICATION = 'working_bikes.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv(PROJECT_VARIABLE_PATTERN.format('DATABASE_NAME')),
        'USER': os.getenv(PROJECT_VARIABLE_PATTERN.format('DATABASE_USER')),
        'PASSWORD': os.getenv(PROJECT_VARIABLE_PATTERN.format('DATABASE_PASSWORD')),
        'HOST': os.getenv(PROJECT_VARIABLE_PATTERN.format('DATABASE_HOST'), 'localhost'),
        'PORT': os.getenv(PROJECT_VARIABLE_PATTERN.format('DATABASE_PORT'), 3306),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = os.getenv(PROJECT_VARIABLE_PATTERN.format('STATIC_URL'), '/static/')
STATIC_ROOT = os.getenv(PROJECT_VARIABLE_PATTERN.format('STATIC_ROOT'), 'static')
MEDIA_URL = os.getenv(PROJECT_VARIABLE_PATTERN.format('MEDIA_URL'), '/media/')
MEDIA_ROOT = os.getenv(PROJECT_VARIABLE_PATTERN.format('MEDIA_ROOT'), 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner' 

NOSE_ARGS = [
    '-d',
    '--quiet',
    '--with-fixture-bundling',
    '--with-coverage',
    '--cover-package=.',
    '--cover-erase',
    '--cover-branches',
]
