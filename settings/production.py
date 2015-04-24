from settings.defaults import *

STATIC_ROOT = '/data/www/buzzart/static'
MEDIA_ROOT = '/data/www/buzzart/media'
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['mijn.buzzart.nl']

GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-55846562-2'
GOOGLE_ANALYTICS_DOMAIN = 'mijn.buzzart.nl'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dj_buzzart',                          # Or path to database file if using sqlite3.
        'USER': 'buzzmin',                    # Not used with sqlite3.
        'PASSWORD': 'rDGnTkUP',               # Not used with sqlite3.
        'HOST': '10.0.7.101',                 # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
    },
}

NOTIFIER_BCC = 'dropbox@49216645.fundament.capsulecrm.com'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        }
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/data/www/buzzart/buzzart.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'WARNING',
        },
        'buzzart': {
            'handlers': ['file'],
            'level': 'WARNING',
        },
    }
}