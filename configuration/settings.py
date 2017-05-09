import os

from django.http import Http404

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_NAME = 'WORKING_BIKES'
PROJECT_VARIABLE_PATTERN = '_'.join((PROJECT_NAME, '{}'))


def get_env_var(var_name, default=None):
    return os.getenv(PROJECT_VARIABLE_PATTERN.format(var_name), default)


SECRET_KEY = get_env_var('SECRET_KEY')

DEBUG = get_env_var('DEBUG', False) == 'TRUE'

ALLOWED_HOSTS = get_env_var('ALLOWED_HOSTS', '*').split(',')

ADMINS = (
    ('Dane Hillard', 'github@danehillard.com'),
)

MANAGERS = ADMINS

ADMIN_URL = get_env_var('ADMIN_URL', r'^admin/')

LOGIN_REDIRECT_URL = '/volunteer/profile/'
LOGIN_URL = '/volunteer/login/'
LOGOUT_URL = '/volunteer/logout/'

BUILTIN_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MY_APPS = [
    'volunteer',
]

THIRD_PARTY_APPS = [
    'explorer',
]

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + MY_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
)

ROLLBAR = {
    'access_token': get_env_var('ROLLBAR_ACCESS_TOKEN'),
    'environment': 'development' if DEBUG else 'production',
    'root': BASE_DIR,
    'exception_level_filters': [
        (Http404, 'ignored'),
    ]
}

ROOT_URLCONF = 'configuration.urls'
WSGI_APPLICATION = 'configuration.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_var('DATABASE_NAME'),
        'USER': get_env_var('DATABASE_USER'),
        'PASSWORD': get_env_var('DATABASE_PASSWORD'),
        'HOST': get_env_var('DATABASE_HOST', 'localhost'),
        'PORT': get_env_var('DATABASE_PORT', 3306),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = get_env_var('STATIC_URL', '/static/')
STATIC_ROOT = get_env_var('STATIC_ROOT', 'static')
MEDIA_URL = get_env_var('MEDIA_URL', '/media/')
MEDIA_ROOT = get_env_var('MEDIA_ROOT', 'media')

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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
