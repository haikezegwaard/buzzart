from facebookads.api import FacebookAdsApi
from facebookads import objects
from django.conf import settings
from models import FacebookAdsSettings
from urlparse import parse_qs, urlparse
import requests
import logging
from datetime import datetime, timedelta
import hmac
import hashlib


class FacebookAdsManager:

    def __init__(self, token):
        """
        Initialize the manager, create a long lived token and store it
        """
        self.graph_base_url = 'https://graph.facebook.com/'
        self.api_version = 'v2.2'
        self.logger = logging.getLogger(__name__)
        if FacebookAdsSettings.objects.all().count() == 0:
            try:
                self.generate_long_lived_token(token)
            except Exception:
                self.logger.error('Could not generate long lived token')
                pass
        if FacebookAdsSettings.objects.all().count() > 1:
            raise Exception('''Found more than one Facebook Ad access token
                               in the database, this should not happen!''')
        my_app_id = settings.FACEBOOK_ADS_APP_ID
        my_app_secret = settings.FACEBOOK_ADS_APP_SECRET
        my_access_token = self.get_stored_token()
        try:
            FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
        except Exception:
            self.logger.error('Could not initialize FB Ads API')

    def get_campaign_stats(self, cid):
        campaign = objects.AdCampaign(cid)
        for item in campaign.get_ad_sets(fields=[objects.AdSet.Field.name]):
            self.logger.debug("adset: {}".format(item[objects.AdSet.Field.name]))
            adset = objects.AdSet(item[objects.AdSet.Field.id])
            adgroups = adset.get_ad_groups(fields=[objects.AdGroup.Field.name])
            for ad in adgroups: #ad = objects.AdGroup(ad[objects.AdGroup.Field.id])
                self.logger.debug("adgroup: {}".format(ad[objects.AdGroup.Field.name]))
                self.logger.debug(ad.get_stats())

        return 'foo'

    def get_stored_token(self):
        """
        Get the stored access token, there should be only one.
        This is a long lived token.
        """
        try:
            fbsettings = FacebookAdsSettings.objects.first()
            return fbsettings.access_token
        except:
            return False


    def get_app_proof(self):
        """
        Generate the App secret proof, this is sent with every request
        when an app in facebook has configured 'App secret proof=yes'
        It is ment for extra security when calling the API from a server
        """
        key = settings.FACEBOOK_ADS_APP_SECRET
        data = self.get_stored_token()
        return hmac.new(key, data, hashlib.sha256).hexdigest()

    def generate_long_lived_token(self, short_token):
        """
        exchange (short lived) access token for a long lived one (60 days?)
        store the long lived token in the db
        """
        url = 'https://graph.facebook.com/oauth/access_token'
        response = requests.get(url, params={'client_id': settings.FACEBOOK_ADS_APP_ID,
                                             'client_secret': settings.FACEBOOK_ADS_APP_SECRET,
                                             'grant_type': 'fb_exchange_token',
                                             'fb_exchange_token': short_token})
        self.logger.debug(response.content)
        dictresponse = parse_qs(urlparse('?{}'.format(response.content)).query, keep_blank_values=True)
        self.logger.debug(dictresponse)
        if response.status_code == 200:
            token = dictresponse.get('access_token')[0]
            expires = datetime.now() + timedelta(seconds=int(dictresponse.get('expires')[0]))
            FacebookAdsSettings.objects.create(access_token=token, expires=expires)
            return token
        else:
            raise Exception('Could not fetch token, http code: {}'.format(response.status_code))


    def API_call(self, graph_object, pars={}, method='GET'):
        """
        Generic method for calling the facebook API. It sends a request
        to the given object with given parameters, and adds security.
        Access token and app secret proof are added to params dict
        Default method is GET, can be customized.
        """
        url = '{}{}/{}'.format(self.graph_base_url, self.api_version, graph_object)
        pars['access_token'] = self.get_stored_token()
        pars['appsecret_proof'] = self.get_app_proof()
        if method == 'GET':
            return requests.get(url, params=pars)
        if method == 'POST':
            return requests.post(url, params=pars)
        return None # this should not happen










