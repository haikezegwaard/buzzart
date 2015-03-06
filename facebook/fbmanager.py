import json
import logging
import requests
import pprint
import models
from social.apps.django_app.utils import load_strategy
from django.contrib.auth.models import User
import settings
import time


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
        url = '{}{}/{}/insights/page_fans_gender_age'.format(self.GRAPH_URL,self.GRAPH_VERSION, project.fanpage_id)
        result = requests.get(url,params={'access_token':project.fanpage_token}).json()
        data = result.get('data').pop().get('values')
        lastvalues = max(data,key=lambda item:item['end_time']) #compare based on EACH items 'end_time' field
        return lastvalues.get('value')

    def get_likes_sex_age_spread_sorted(self, project):
        """
        Return age / sex spread formatted for use in Google Chart
        """
        agesexspread = self.get_likes_sex_age(project)
        if agesexspread == []:
            return []
        fullspread = {}
        for k, v in agesexspread.items():
            if k.startswith('M.'):
                testkey = u'F.{}'.format(k[2:])
            if k.startswith('F.'):
                testkey = u'M.{}'.format(k[2:])
            if k.startswith('U.'):
                continue
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
    
    def get_page_impressions(self, project, date_start, date_end):
        """
        Return impressions for fanpage
        """        
        url = '{}{}/{}/insights/page_impressions?period=day&since={}&limit=100'.format(
                self.GRAPH_URL, self.GRAPH_VERSION, project.fanpage_id, '1418015467')
        json = requests.get(url,params={'access_token':project.fanpage_token}).json()
        data = json.get('data').pop().get('values')
        result = {}
        for item in data:
            result[item.get('end_time')] = item.get('value')
        return result
    
    def get_page_engaged(self, project, date_start, date_end):
        """
        The number of people who engaged with your Page. 
        Engagement includes any click
        """
        url = '{}{}/{}/insights/page_engaged_users?period=day&since={}&limit=100'.format(
                self.GRAPH_URL, self.GRAPH_VERSION, project.fanpage_id, '1418015467')
        json = requests.get(url,params={'access_token':project.fanpage_token}).json()
        data = json.get('data').pop().get('values')
        result = {}
        for item in data:
            result[item.get('end_time')] = item.get('value')
        return result
    
    def get_page_fans(self, project, date_start, date_end):
        """
        The number of likes of the fanpage
        """
        url = '{}{}/{}/insights/page_fans?period=lifetime&since={}&limit=100'.format(
                self.GRAPH_URL, self.GRAPH_VERSION, project.fanpage_id, '1418015467')
        json = requests.get(url,params={'access_token':project.fanpage_token}).json()
        data = json.get('data').pop().get('values')
        result = {}
        for item in data:
            result[item.get('end_time')] = item.get('value')
        return result
    
    def get_page_overview(self, project, date_start, date_end):
        fans = self.get_page_fans(project, date_start, date_end)
        impressions = self.get_page_impressions(project, date_start, date_end)
        engaged = self.get_page_engaged(project, date_start, date_end)
        result = []
        for key, value in impressions.items():
            result.append({'date': key,'impressions': value,'fans':
                           fans.get(key),'engaged': engaged.get(key)})
        return result
        
        

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
        user = User.objects.get(username=settings.ADMIN_USER) #this should not be static
        #get the oath2 token for user haike
        social = user.social_auth.get(provider='facebook')
        strategy = load_strategy(backend='facebook')
        social.refresh_token(strategy)
        return social.extra_data['access_token']
