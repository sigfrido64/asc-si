# coding=utf-8
"""
Django settings for si project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/

Utente Amministrativo : admin - radice
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from decouple import config
from unipath import Path
import dj_database_url


BASE_DIR = Path(__file__).parent
PROJECT_DIR = Path(__file__).parent
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
DEBUG_PRINT = config('DEBUG_PRINT', default=False, cast=bool)


"""
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            TEMPLATE_PATH,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'si.sig_context_processor.permissions',
            ],
            'debug': True,
        },
    },
]
"""
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_DIR.parent.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'si.sig_context_processor.permissions',
            ],
            'debug': True,
        },
    },
]


ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])


# Application definition
# Admin password = radice
# Ho tolto 'docusign'
# 'corsi',
#    'aziende',
# 'op',
# iniziative
# 'sifilesmanager',


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'import_export',
    'debug_toolbar',
    'tasker',
    'si.apps.siprof',
    'si.apps.ordacq',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'si.urls'

WSGI_APPLICATION = 'si.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '',
    },
}


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'IT'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

# Lo lascio falso così prende per buone le cose che scrivo e non ci mette del suo per convertirle in UTC.
# Maggio 2016 : Il coglione quando salva converte in UTC e poi non riconverte !! Pertanto se lo lascio a True
# ad ogni salvataggio mi andava indietro di un'ora.
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
# STATIC_ROOT = PROJECT_DIR.child('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    PROJECT_DIR.parent.child('static'),
)

MEDIA_ROOT = PROJECT_DIR.parent.parent.child('media')
MEDIA_URL = '/uploads/'


"""
STATIC_URL = '/static/'
STATIC_PATH = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    STATIC_PATH,
)

#
# Qui invece salvo i file di cui faccio l'upload.
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = 'uploads/'
"""

#
# E qui memorizzo i dati del mio filesystem.
SIFILEDATA_ROOT = os.path.join(BASE_DIR, 'data')
SIFILEDATA_URL = '/data/'

LOGIN_REDIRECT_URL = '/si/'
LOGIN_URL = "/si/login/"

#
# Lista indirizzi interni su cui abilitare il debug.
INTERNAL_IPS = ['127.0.0.1']

#
# Pannelli da abilitare per Django Debug Toolbar
#
DEBUG_TOOLBAR_PANELS = [
    'ddt_request_history.panels.request_history.RequestHistoryPanel',  # Here it is
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

#
# Aggiunge il supporto di Ajax alla Toolbar
#
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': config('SHOW_TOOLBAR_CALLBACK', cast=lambda v: v if v != '' else lambda r: False),
}

#
# Dice ad import_export di usare le transazioni quando importa.
# Lo setto per essere tranquillo visto che, di default, è settato a false.
#
IMPORT_EXPORT_USE_TRANSACTIONS = True
