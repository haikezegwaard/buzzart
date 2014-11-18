from django.shortcuts import render_to_response
from django.conf import settings
from facebookads import objects
from facebookads.api import FacebookAdsApi
from fbadsmanager import FacebookAdsManager
import logging
# Create your views here.

logger = logging.getLogger(__name__)


def index(request):
    fbman = FacebookAdsManager(settings.FACEBOOK_ADS_ACCESS_TOKEN)
    stats = fbman.get_campaign_stats()
    return render_to_response('facebookAds/index.html',
                              {"stats": stats},
                              content_type="text/html")
