from settings.defaults import *
#################
# DEBUG TOOLBAR #
#################
DEBUG_TOOLBAR_PATCH_SETTINGS = False  # explicit setup

STATIC_ROOT = '/data/www/buzzart/static'

def _show_toolbar(request):
    # avoid executing in tests (which sets DEBUG to False)
    if request.is_ajax():
        return False
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if 'MSIE' in user_agent:
        return False
    from django.conf import settings
    return settings.TEMPLATE_DEBUG
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'settings.defaults._show_toolbar',  # 'debug_toolbar.middleware.show_toolbar'
    'INTERCEPT_REDIRECTS': False,
}

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
