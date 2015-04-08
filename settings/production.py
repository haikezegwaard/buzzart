from settings.defaults import *

STATIC_ROOT = '/data/www/buzzart/static'
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dj_buzzart',                    # Or path to database file if using sqlite3.
        'USER': 'buzzmin',                    # Not used with sqlite3.
        'PASSWORD': 'rDGnTkUP',               # Not used with sqlite3.
        'HOST': '10.0.7.101',                 # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
    },
}

NOTIFIER_BCC = 'dropbox@49216645.fundament.capsulecrm.com'