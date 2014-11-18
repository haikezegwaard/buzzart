from django.shortcuts import render_to_response
from django.conf import settings
from facebookads import objects
from facebookads.api import FacebookAdsApi
import logging
# Create your views here.

logger = logging.getLogger(__name__)


def index(request):
    FacebookAdsApi.init(settings.FACEBOOK_ADS_APP_ID,
                        settings.FACEBOOK_ADS_APP_SECRET,
                        settings.FACEBOOK_ADS_ACCESS_TOKEN)
    me = objects.AdUser(fbid='me')
    my_accounts = list(me.get_ad_accounts())
    logger.debug(my_accounts)
    return render_to_response('facebookAds/index.html',
                              {"my_accounts": my_accounts},
                              content_type="text/html")
