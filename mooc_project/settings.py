"""
Django settings for mooc_project project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't0!344w2guwb%ro5-1w*q6c6&@ufx)c!34#8fixz!*j99o%vyy'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = (os.environ.get('DEBUG') == 'True')
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','159.223.14.73','www.productivvacademy.com','.productivvacademy.com']
# ALLOWED_HOSTS = ['127.0.0.1']  # allow all access

AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'courses.apps.CoursesConfig',
    'operation.apps.OperationConfig',
    'organizations.apps.OrganizationsConfig',
    'xadmin.apps.XAdminConfig',
    'captcha',
    'crispy_forms',
    'pure_pagination',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Make the UserProfile we defined in users.models take effect
AUTH_USER_MODEL = 'users.UserProfile'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
MIDDLEWARE_CLASSES = (
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware',)

ROOT_URLCONF = 'mooc_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'mooc_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase3',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
        }
    }
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'productivvacademy',
        'USER': 'richard',
        'PASSWORD': 'Lamperouge@123',
        'HOST': 'localhost',
        'PORT': '',
        }
    }
# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_L10N = True

USE_TZ = False

PAYTM_MERCHANT_ID = 'LPsQZA34058459749141'

PAYTM_SECRET_KEY = 'C2AW4NCiCdXKCT4I'

PAYTM_WEBSITE = 'DEFAULT'

PAYTM_CHANNEL_ID = 'WEB'

PAYTM_INDUSTRY_TYPE_ID = 'Retail'

#testing
# PAYTM_MERCHANT_ID = 'zsnrbl00943963013177'
# PAYTM_SECRET_KEY = '%Cc@5Nmu%UaCoMZb'
# PAYTM_WEBSITE = 'WEBSTAGING'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'richardrozario.a@gmail.com'
EMAIL_HOST_PASSWORD = 'twloczewhbmtkmjr'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_FROM = 'richardrozario.a@gmail.com'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.office365.com'
# EMAIL_HOST_USER = 'admin@productivvacademy.com'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD = 'Lamperouge@123'
# EMAIL_PORT = 465
# EMAIL_USE_SSL = False
# EMAIL_USE_TLS = True
# EMAIL_FROM = 'admin@productivvacademy.com'

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,
    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

django_heroku.settings(locals())
  