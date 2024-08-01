from pathlib import Path
import socket
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MONITDJ_VERSION = "0.0.1"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p==v1p#_l&weoi%c(oh_s0l-jw%v&3t086wxic3clim9tb@gy@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '0.0.0.0', '192.168.30.14', '192.168.1.113', '192.168.56.1']


# Application definition

INSTALLED_APPS = [
    'main',
    'alerts',
    'django_bootstrap5',
    'bootstrap_modal_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    "mathfilters",
    #"huey.contrib.djhuey"
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware', # for static file serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]


ROOT_URLCONF = 'monitdj.urls'

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

WSGI_APPLICATION = 'monitdj.wsgi.application'


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": "mb",
#         "USER": "monitbee",
#         "PASSWORD": "monitbee",
#         "HOST": "localhost",
#         "PORT": 5432
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True


# for DEV deployment
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'main/static'),]




# for Prod Deployment
# STATIC_ROOT = os.path.join(BASE_DIR, 'static',)

CACHES = {
   "default": {
       "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
       "LOCATION": "monit-data"
   }
}

INTERNAL_IPS = ["127.0.0.1"]
DEBUG_TOOLBAR_CONFIG = {
    'RENDER_PANELS': True,
    'RESULTS_CACHE_SIZE': 100,
    'RESULTS_STORE_SIZE': 30, # Required for ddt_request_history
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}
