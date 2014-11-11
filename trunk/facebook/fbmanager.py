import json
import logging
import requests
import pprint
import models
from social.apps.django_app.utils import load_strategy
from django.contrib.auth.models import User


class FacebookManager:
    """
    Interface for accessing the Facebook Insights api
    """
    GRAPH_URL = 'https://graph.facebook.com/'
    GRAPH_VERSION = 'v2.2'

    logger = logging.getLogger(__name__)

    def get_likes_sex_age(self, project):
        """
        Return sex / age spread for likes of page
        """
        url = '{}{}/insights/page_fans_gender_age?access_token={}'.format(self.GRAPH_URL, project.fanpage_id, project.fanpage_token)
        result = self.do_request(url)
        data = result.get('data').pop().get('values')

        lastvalues = max(data,key=lambda item:item['end_time']) #compare based on EACH items 'end_time' field
        return lastvalues.get('value')

    def get_likes_sex_age_spread_sorted(self, project):
        """
        Return age / sex spread formatted for use in Google Chart
        """
        agesexspread = self.get_likes_sex_age(project)
        fullspread = {}
        for k, v in agesexspread.items():
            if k.startswith('M.'):
                testkey = u'F.{}'.format(k[2:])
            if k.startswith('F.'):
                testkey = u'M.{}'.format(k[2:])
            if testkey not in agesexspread:
                fullspread[testkey] = 0
            fullspread[k] = v
        self.logger.debug(fullspread)

        male = {k[2:]: v for k, v in fullspread.items() if k.startswith('M.')}
        female = {k[2:]: v for k, v in fullspread.items() if k.startswith('F.')}

        d = {}
        for i in male.keys():
            d[i] = [male[i], female[i]]

        return (sorted(d.items()))

    def get_access_token_token(self, page):
        """
        Return permanent access token for page/insights access
        """
        url = '{}{}/{}'.format(self.GRAPH_URL, self.GRAPH_VERSION, page)
        url += '?fields=access_token&access_token={}'.format(self.get_fb_user_token())
        r = requests.get(url).json()
        self.logger.debug('request: {}'.format(url))
        self.logger.debug(r)
        return r.get('access_token')

    def get_fb_user_token(self):
        """
        Retrieve facebook user token from python-social-auth lib
        """
        user = User.objects.get(username="haike") #this should not be static
        #get the oath2 token for user haike
        social = user.social_auth.get(provider='facebook')
        strategy = load_strategy(backend='facebook')
        social.refresh_token(strategy)
        return social.extra_data['access_token']
