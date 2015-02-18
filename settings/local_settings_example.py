from settings.defaults import *
#################
# DEBUG TOOLBAR #
#################
DEBUG_TOOLBAR_PATCH_SETTINGS = False  # explicit setup


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

DEBUG = True

TEMPLATE_DEBUG = True

# python-social-auth settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '799281546392-hcq2ns4i3sj3dsmlhlqhlqem9h78evkb.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'BF7XhVMue2TXLfF5RbpGXeLK'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['https://www.googleapis.com/auth/analytics.readonly']
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'access_type': 'offline'}