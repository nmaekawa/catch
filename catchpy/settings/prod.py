"""
Django settings for catch project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = 'catchpy'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('CATCHPY_SECRET_KEY', 'CHANGE_ME')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ.get(
    'CATCHPY_ALLOWED_HOSTS', 'localhost 127.0.0.1').split()


# Application definition

INSTALLED_APPS = [
    'anno.apps.AnnoConfig',
    'consumer.apps.ConsumerConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'consumer.jwt_middleware.jwt_middleware',
]

ROOT_URLCONF = PROJECT_NAME + '.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('CATCHPY_DB_NAME', 'catchpy'),
        'USER': os.environ.get('CATCHPY_DB_USER', 'catchpy'),
        'PASSWORD': os.environ.get('CATCHPY_DB_PASSWORD', 'catchpy'),
        'HOST': os.environ.get('CATCHPY_DB_HOST', 'localhost'),
        'PORT': os.environ.get('CATCHPY_DB_PORT', '5432'),
        'ATOMIC_REQUESTS': False,
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
"""
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
"""

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('CATCHPY_STATIC_ROOT', os.path.join(BASE_DIR, 'static/'))


# Logging config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s|%(levelname)s [%(filename)s:%(funcName)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        },
        'errorfile_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'filename': 'catchpy_errors.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 7,
            'encoding': 'utf8',
        },
    },
    'loggers': {
        'anno': {
            'level': 'DEBUG',
            'handlers': ['console', 'errorfile_handler'],
            'propagate': True
        },
        'consumer': {
            'level': 'DEBUG',
            'handlers': ['console', 'errorfile_handler'],
            'propagate': True
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    }
}

compat_mode = os.environ.get('CATCHPY_COMPAT_MODE', 'false')
if compat_mode.lower() == 'true':
    CATCH_RESPONSE_FORMAT = 'ANNOTATORJS_FORMAT'
else:
    CATCH_RESPONSE_FORMAT = 'CATCH_ANNO_FORMAT'

# max number of rows to be returned in a search request
CATCH_RESPONSE_LIMIT = 200
