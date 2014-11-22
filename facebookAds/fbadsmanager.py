from facebookads.api import FacebookAdsApi
from facebookads import objects
from django.conf import settings
from facebookads.objects import AdCampaign, ReportStats
from models import FacebookAdsSettings
import requests
import logging
import json


class FacebookAdsManager:

    def __init__(self, token):
        self.logger = logging.getLogger(__name__)

        long_token = None
        if FacebookAdsSettings.objects.all().count() == 0:
            long_token = self.generate_long_lived_token(token)
        else:
            fbsettings = FacebookAdsSettings.objects.first()
            long_token = fbsettings.access_token
        FacebookAdsApi.init(settings.FACEBOOK_ADS_APP_ID,
                            settings.FACEBOOK_ADS_APP_SECRET,
                            long_token)

    def get_campaign_stats(self):
        #my_account = objects.AdAccount('act_52022373')
        #result = my_account.get_report_stats(fields=['date-preset'],params=['last_28_days'])
        url = '''https://graph.facebook.com/act_52022373/reportstats?
                 data_columns=['account_id','spend','action_values']&
                 date_preset=last_7_days&
                 actions_group_by=['action_type']&
                 access_token={}'''.format(self.get_stored_token())
        response = requests.get(url,params={'access_token': self.get_stored_token(),
                                            'data_columns': "['account_id','spend','action_values']",
                                            'date_preset' : 'last_7_days',
                                            'actions_group_by': "['action_type']"})
        """
        result = ''
        for campaign in my_account.get_ad_campaigns(fields=[AdCampaign.Field.name]):

            for stat in campaign.get_stats(fields=[
                'impressions',
                'clicks',
                'spent',
                'unique_clicks',
                'actions',
                'start_time',
                'end_time'
            ]):
                campaign_name = campaign[campaign.Field.name].encode('utf-8')
                result = '{}<br />{}<br/>'.format(result, campaign_name)
                for statfield in stat:
                    result = "{}<br />{}{}".format(result, statfield, stat[statfield])
                break
            break
        """
        return response

    def get_stored_token(self):
        fbsettings = FacebookAdsSettings.objects.first()
        return fbsettings.access_token

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
        from urlparse import parse_qs, urlparse
        dictresponse = parse_qs(urlparse('?{}'.format(response.content)).query, keep_blank_values=True)
        self.logger.debug(dictresponse)
        if response.status_code == 200:
            token = dictresponse.get('access_token')[0]
            from datetime import datetime, timedelta
            expires = datetime.now() + timedelta(seconds=int(dictresponse.get('expires')[0]))

            FacebookAdsSettings.objects.create(access_token=token, expires=expires)
            return token
        else:
            raise Exception('Could not fetch token, http code: {}'.format(response.status_code))









