from pathlib import Path

import os

# =====================================

# BASE DIRECTORY

# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================

# SECURITY

# =====================================

SECRET_KEY = 'django-insecure-change-this-key'

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [

    'https://web-production-ed615.up.railway.app',

    'https://*.up.railway.app',

]

# =====================================

# INSTALLED APPS

# =====================================

INSTALLED_APPS = [

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    'myapp',

]

# =====================================

# MIDDLEWARE

# =====================================

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

# =====================================

# URL

# =====================================

ROOT_URLCONF = 'myproject.urls'

# =====================================

# TEMPLATES

# =====================================

TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

            ],

        },

    },

]

# =====================================

# WSGI

# =====================================

WSGI_APPLICATION = 'myproject.wsgi.application'

# =====================================

# DATABASE

# =====================================

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',

    }

}

# =====================================

# PASSWORD

# =====================================

AUTH_PASSWORD_VALIDATORS = []

# =====================================

# LANGUAGE

# =====================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_TZ = True

# =====================================

# STATIC FILES

# =====================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [

    BASE_DIR / 'static',

]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =====================================

# MEDIA FILES

# =====================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# =====================================

# LOGIN

# =====================================

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/home/'

LOGOUT_REDIRECT_URL = '/login/'

# =====================================

# DEFAULT PK

# =====================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'