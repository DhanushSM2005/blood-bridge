import os
import pymysql
import dj_database_url
from pathlib import Path

# 1. DATABASE COMPATIBILITY
# Ensures pymysql works with Django 6.x
pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

# 2. SECURITY
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-change-this')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

# 3. APPLICATION DEFINITION
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'Frontend',
]

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

ROOT_URLCONF = 'Blood_Bridge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'Frontend' / 'templates'],
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

# 4. DATABASE CONFIGURATION
# Prioritize Railway's individual variables if DATABASE_URL is missing
if os.environ.get('MYSQLHOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('MYSQLDATABASE'),
            'USER': os.environ.get('MYSQLUSER'),
            'PASSWORD': os.environ.get('MYSQLPASSWORD'),
            'HOST': os.environ.get('MYSQLHOST'),
            'PORT': os.environ.get('MYSQLPORT'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
else:
    # Fallback to DATABASE_URL or Local Development
    DATABASES = {
        'default': dj_database_url.config(
            default='mysql://bloodbridge_user:BloodBridge@2026@localhost:3306/blood_bridge_db',
            conn_max_age=600,
        )
    }

# 5. STATIC FILES
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'