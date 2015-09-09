from settings.defaults import *
#################
# DEBUG TOOLBAR #
#################
DEBUG_TOOLBAR_PATCH_SETTINGS = False  # explicit setup
DEBUG = True
TEMPLATE_DEBUG = True

STATIC_ROOT = '/data/www/buzzart/static'
MEDIA_ROOT = '/data/www/buzzart_media'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'buzzart',                    # Or path to database file if using sqlite3.
        'USER': 'buzzmin',                    # Not used with sqlite3.
        'PASSWORD': '29KAJrKu',               # Not used with sqlite3.
        'HOST': '87.233.7.136',               # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
    },
}

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
            'filename': os.path.join(PROJECT_ROOT,'buzzart.log'),
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'buzzart': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
