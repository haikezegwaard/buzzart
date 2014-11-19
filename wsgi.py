"""
WSGI config for monitor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

# put the Django project on sys.path
PROJECT_ROOT = os.path.normpath(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


