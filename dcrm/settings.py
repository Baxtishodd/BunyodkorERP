from pathlib import Path
import os
from dotenv import load_dotenv
import environ
from django.utils.translation import gettext_lazy as _
from django.conf.global_settings import AUTH_USER_MODEL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL

import dj_database_url


# load_dotenv(os.path.join(BASE_DIR, ".env"))

# .env ni yuklash — faqat 1 marta
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"

# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.101.76', 'https://bunyodkorerp-production.up.railway.app/']

ALLOWED_HOSTS = ['bunyodkorerp.onrender.com', 'localhost', '127.0.0.1']
# ALLOWED_HOSTS = ['*']

# --- DATABASES ---

if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv("ENGINE", "django.db.backends.mysql"),
            'NAME': os.getenv("DB_NAME"),
            'USER': os.getenv("DB_USER"),
            'PASSWORD': os.getenv("DB_PASSWORD"),
            'HOST': os.getenv("DB_HOST", "localhost"),
            'PORT': os.getenv("DB_PORT", "3306"),
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

INSTALLED_APPS += [
    'django.contrib.sites',
    'imagekit',
]
SITE_ID = 1

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # my edit
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

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Path to locale directory
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = 'login'  # Fixed from LOGIN to LOGIN_URL
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'


# Media files
DEFAULT_FILE_STORAGE = "dcrm.storages.SupabaseStorage"
MEDIA_URL = f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/{os.getenv('SUPABASE_BUCKET')}/"

# MEDIA_ROOT = None
# fallback uchun kerak
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

from django.core.files.storage import default_storage
print(f"🧠 Hozirgi storage b: {DEFAULT_FILE_STORAGE}")
print(f"🧠 Django ishlatayotgani: {default_storage.__class__}")

