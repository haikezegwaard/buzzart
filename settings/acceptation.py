from settings.defaults import *
#################
# DEBUG TOOLBAR #
#################
DEBUG_TOOLBAR_PATCH_SETTINGS = False  # explicit setup
DEBUG = True
TEMPLATE_DEBUG = True

STATIC_ROOT = '/data/www/buzzart/static'
MEDIA_ROOT = '/data/www/buzzart/media'

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
