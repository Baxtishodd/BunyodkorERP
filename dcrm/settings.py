from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _
from django.conf.global_settings import AUTH_USER_MODEL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
import environ
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env("DEBUG")

# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.101.76', 'https://bunyodkorerp-production.up.railway.app/']

ALLOWED_HOSTS = ['*']

# --- DATABASES ---
if os.environ.get("DATABASE_URL"):
    # 🚀 Railway (PostgreSQL) uchun
    DATABASES = {
        "default": dj_database_url.config(conn_max_age=600)
    }
else:
# 💻 Lokal uchun (MySQL yoki lokal DB)
    DATABASES = {
        'default': {
            'ENGINE': env("ENGINE", default='django.db.backends.mysql'),
            'NAME': env("DB_NAME"),
            'USER': env("DB_USER"),
            'PASSWORD': env("DB_PASSWORD"),
            'HOST': env("DB_HOST", default='localhost'),
            'PORT': env("DB_PORT", default='3306'),
        }
    }


# Applications definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'django.contrib.humanize',

    # my apps
    'accounts',
    'website',
    'plm',
]

INSTALLED_APPS += ['django.contrib.sites']
SITE_ID = 1

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # my edit
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'dcrm.urls'

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

WSGI_APPLICATION = 'dcrm.wsgi.application'

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-US'

# Add your supported languages
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('uz', _('Uzbek')),
]

USE_L10N = True
USE_I18N = True

USE_TZ = True
TIME_ZONE = 'Asia/Tashkent'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'  # Note the leading slash
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Add this line
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Path to locale directory
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = 'login'  # Fixed from LOGIN to LOGIN_URL
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
