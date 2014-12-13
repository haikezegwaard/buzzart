from django.shortcuts import render_to_response
from django.conf import settings
from facebookads import objects
from facebookads.api import FacebookAdsApi
from fbadsmanager import FacebookAdsManager
from facebookads.objects import AdCampaign
import logging
from django.conf import settings
# Create your views here.

logger = logging.getLogger(__name__)
fbman = FacebookAdsManager(settings.FACEBOOK_ADS_ACCESS_TOKEN)


def index(request):
    stats = fbman.get_campaign_stats('6010164041427')
    return render_to_response('facebookAds/index.html',
                              {"stats": "check the logs"},
                              content_type="text/html")

def asyncjob(request, job):
    stats = fbman.get_async_report(job)
    return render_to_response('facebookAds/index.html',
                              {"stats": stats.content},
                              content_type="text/html")

def jobstatus(request, job):
    stats = fbman.get_job_status(job)
    return render_to_response('facebookAds/index.html',
                              {"stats": stats.content},
                              content_type="text/html")

