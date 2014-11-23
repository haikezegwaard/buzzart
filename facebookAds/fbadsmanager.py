from facebookads.api import FacebookAdsApi
from facebookads import objects
from django.conf import settings
from facebookads.objects import AdCampaign, ReportStats
from models import FacebookAdsSettings
from urlparse import parse_qs, urlparse
import requests
import logging
import json
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
            self.generate_long_lived_token(token)
        if FacebookAdsSettings.objects.all().count() > 1:
            raise Exception('''Found more than one Facebook Ad access token
                               in the database, this should not happen!''')


    def get_async_report(self, job):
        params={'report_run_id': job}
        graph_object='act_52022373/reportstats'
        return self.API_call(graph_object, params)

    def get_campaign_stats(self, async='false'):
        graph_object = 'act_52022373/reportstats'
        pars={'data_columns': "['account_id','spend','action_values']",
              'time_ranges': "[{'day_start':{'day':1,'month':3,'year':2010},'day_stop':{'day':27,'month':3,'year':2012}}]",
              'actions_group_by': "['action_type']"}
        if async == 'true':
            pars['async'] = 'true'
            response = self.API_call(graph_object, pars, 'POST')
        else:
            response = self.API_call(graph_object, pars)
            if 'Too old' in response.content:
                return self.get_campaign_stats('true')
        return response

    def get_job_status(self, job):
        return self.API_call(job)

    def get_stored_token(self):
        """
        Get the stored access token, there should be only one.
        This is a long lived token.
        """
        fbsettings = FacebookAdsSettings.objects.first()
        return fbsettings.access_token

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










