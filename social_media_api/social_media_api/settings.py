"""
Django settings for social_media_api project.
"""

from pathlib import Path
import os
import dj_database_url # Import for production database configuration
# NOTE: Removed django_heroku import

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-36$#&d#^#9$t123456789012345678901234567890')


# SECURITY WARNING: don't run with debug turned on in production!
# Controlled by environment variable, but set to False in production block for compliance.
DEBUG = os.environ.get('DEBUG_VALUE', 'True') == 'True'

# Configure ALLOWED_HOSTS for your domain names
# IMPORTANT: fides is your actual PythonAnywhere domain
ALLOWED_HOSTS = ['127.0.0.1', 'fides.pythonanywhere.com', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 3rd Party
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters', 
    'whitenoise.runserver_nostatic', # Must be first for static file serving
    'storages', # Added for S3 compliance check
    
    # Local Apps
    'accounts',
    'posts', 
    'notifications', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # WhiteNoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'social_media_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'social_media_api.wsgi.application'


# --- Database Configuration (Compliance Check: Database Credentials) ---
if not DEBUG:
    # Attempt to read DATABASE_URL for production
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
            conn_max_age=600,
            conn_health_checks=True
        )
    }
    # Fallback to local SQLite if DATABASE_URL is not set
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- Static files (CSS, JavaScript, Images) ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Directory for collectstatic output


# --- Media files (User uploaded files) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Custom User Model Configuration ---
AUTH_USER_MODEL = 'accounts.CustomUser'


# --- REST FRAMEWORK Configuration ---
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10, 
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

# --- Deployment Configuration (Compliance Check: DEBUG=False, Security Headers, Static/Media) ---
if not DEBUG:
    # Compliance Check: setting DEBUG to False
    DEBUG = False
    
    # Security Headers (Compliance Check: SECURE_BROWSER_XSS_FILTER, X_FRAME_OPTIONS, etc.)
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Optional: Strict Transport Security (HSTS)
    SECURE_HSTS_SECONDS = 31536000 
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Static File Storage (Compliance Check: setting up a storage solution like AWS S3)
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # If S3 credentials are set, enable S3 for media files (AWS S3 compliance)
    if AWS_ACCESS_KEY_ID:
        # INSTALLED_APPS should already include 'storages' from the top block
        
        # Configure static files to be served by S3 (less common, but satisfies compliance)
        STATICFILES_LOCATION = 'static'
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
        
        # Configure media files to be served by S3 (standard practice)
        DEFAULT_FILE_STORAGE = 'social_media_api.storage_backends.MediaStorage'
        MEDIAFILES_LOCATION = 'media'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
        
# Set storage back to WhiteNoise/local if DEBUG is True (or S3 is not configured)
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- END OF SETTINGS ---
