"""
Django settings for TritonValvesTraining project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE = os.path.abspath(os.path.dirname(__name__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-eqwkpmt9sb0hj$_fmb7_ynuawbl2*3a3%qr-iopsc6iu1z#2$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Courses',
    'Users',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'Templates').replace('\\','/'),
)

ROOT_URLCONF = 'TritonValvesTraining.urls'

WSGI_APPLICATION = 'TritonValvesTraining.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'sqlite3.db'),
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
PROJECT_DIR = os.path.dirname(__file__)
STATIC_URL = '/static/'

#STATIC_ROOT = 
MEDIA_URL ='/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
print MEDIA_ROOT

STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static'),)
SESSION_ENGINE = "django.contrib.sessions.backends.cache" 

LOGIN_URL = '/login'
LOGOUT_URL = 'http://127.0.0.1:8000/logout'
LOGIN_REDIRECT_URL = 'http://127.0.0.1:8000/login'


ADMIN_MEDIA_PREFIX = '/static/admin/'

#SESSION_EXPIRE_AT_BROWSER_CLOSE = True

"""
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'testing@example.com'"""


AUTH_PROFILE_MODULE = 'Users.EmployeeInfo'
