"""
Django settings for workingBikes project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '17=$bz2%+)a1jj!7bsdo=#$@c!o5@!(pfx659h(4!^w-0dpxmu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

TEMPLATE_DIRS = (
	BASE_DIR + '/templates',
)

LOGIN_REDIRECT_URL = '/volunteer/profile/'
LOGIN_URL = '/volunteer/login/'
LOGOUT_URL = '/volunteer/logout/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'south',
	'base',
	'volunteer',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'workingBikes.urls'

WSGI_APPLICATION = 'workingBikes.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'working_bikes',
		'USER': 'working_bikes',
		'PASSWORD': 'w0rk1ngb1k35',
		'HOST': '127.0.0.1',
		'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static'

if socket.gethostname() == 'danehillard':
	DEBUG = False
	ALLOWED_HOSTS = ['workingbikes.danehillard.com',]
	DATABASES['default']['HOST'] = 'production.csnsdgwkxnzo.us-east-1.rds.amazonaws.com'
else:
	import mimetypes
	ALLOWED_HOSTS = ['localhost',]

	mimetypes.add_type("image/svg+xml", ".svg", True)
	mimetypes.add_type("image/svg+xml", ".svgz", True)
