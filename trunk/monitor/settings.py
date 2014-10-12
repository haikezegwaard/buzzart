"""
Django settings for monitor project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""


#################
# DEBUG TOOLBAR #
#################
DEBUG_TOOLBAR_PATCH_SETTINGS = False  # explicit setup
def _show_toolbar(request):
    #avoid executing in tests (which sets DEBUG to False)
    if request.is_ajax():
        return False
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if 'MSIE' in user_agent:
        return False
    from django.conf import settings
    return settings.TEMPLATE_DEBUG
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'monitor.settings._show_toolbar',  # 'debug_toolbar.middleware.show_toolbar'
        'INTERCEPT_REDIRECTS': False,
}


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x3q%cez7wog$b++=5%hb=g&v#+ynv_^_js9@x1&$ke55(qn+6m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'niki',
    'monitor',
    'notifier',
    'cyfe',
    'facebook',
    'mcapi',
    'nikiInterest',
    'dashboard',
    'googleAnalytics',
    'social.apps.django_app.default',
    'debug_toolbar',
    'djrill',
    'twitterAnalytics',

)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'social.apps.django_app.context_processors.backends',
    'django.core.context_processors.request',
    'social.apps.django_app.context_processors.login_redirect'
)

#python-social-auth settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '668855476975-5l8p7sua5hp70o0rbisp941dsfk462ki.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'Jfc8k03j8ihL_9U_FgdCvTG4'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['https://www.googleapis.com/auth/analytics.readonly']
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'access_type': 'offline'}

ROOT_URLCONF = 'monitor.urls'

WSGI_APPLICATION = 'wsgi.application'

#djrill settings
MANDRILL_API_KEY = "VWldgpjHZGcavL4jasHiZA"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

ADMIN_MAIL = 'hz@fundament.nl'
NOTIFIER_FROM_MAIL = 'info@fundament.nl'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/opt/buzzart/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/opt/buzzart/media'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'mysite.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'buzzart': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
