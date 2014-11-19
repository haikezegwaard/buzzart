from django.shortcuts import render_to_response
from django.conf import settings
from facebookads import objects
from facebookads.api import FacebookAdsApi
from fbadsmanager import FacebookAdsManager
from facebookads.objects import AdCampaign
import logging
# Create your views here.

logger = logging.getLogger(__name__)


