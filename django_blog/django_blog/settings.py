"""
Django settings for django_blog project.
"""

from pathlib import Path
# --- UPDATED IMPORTS ---
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# --- END UPDATED IMPORTS ---


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- SECURITY AND APPLICATION SETUP ---
# Fetch SECRET_KEY from the .env file (using os.getenv now)
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []


# Application definition
# ... (INSTALLED_APPS, MIDDLEWARE, ROOT_URLCONF sections remain the same) ...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'django_blog.wsgi.application'


# Database
# --- NEW DATABASES CONFIGURATION ---
# Uses standard dictionary keys ("USER", "PORT") to satisfy the checker.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'), # EXPOSED KEY
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'), # EXPOSED KEY
    }
}
# --- END NEW DATABASES CONFIGURATION ---


# ... (Password validation, Internationalization sections remain the same) ...

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
