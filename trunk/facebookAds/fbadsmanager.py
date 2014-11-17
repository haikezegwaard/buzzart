from facebookads.api import FacebookAdsApi
from facebookads import objects
from django.conf import settings


class FacebookAdsManager:

    def __init__(self):
        FacebookAdsApi.init(settings.FACEBOOK_ADS_APP_ID,
                            settings.FACEBOOK_ADS_APP_SECRET,
                            settings.FACEBOOK_ADS_ACCESS_TOKEN)
