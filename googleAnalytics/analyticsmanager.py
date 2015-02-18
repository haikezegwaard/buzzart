from django.contrib.auth.models import User
import requests
import logging
import json
from datetime import datetime
from social.apps.django_app.utils import load_strategy
from datetime import timedelta
from django.conf import settings


class AnalyticsManager:

    GA_REPORTING_URL = 'https://www.googleapis.com/analytics/v3/data/ga?'

    logger = logging.getLogger(__name__)

    GA_NULL_DATE = '2005-01-01'

    def get_weekly_visits(self, viewid, start, end):
        """For convenience only"""
        return self.reporting_API_call(viewid, start, end,
                                       ['sessions', 'pageviews'],
                                       '&sort=ga:date&dimensions=ga:date&max-results=200')

    def get_daily_visits(self, viewid, start, end):
        """Get session count for specific view id  in daterange
        Args:
            viewid: string, id of specific property
            start: datetime, startdate
            end: datetime, enddate in format yyyy-mm-dd
        Returns:
            array of date - count tuples
        """
        start_str = self.google_date(start)
        end_str = self.google_date(end)
        return self.reporting_API_call(viewid, start_str, end_str,
                                       ['sessions'],
                                       '&sort=ga:date&dimensions=ga:date')

    def get_conversion_count(self, viewid, start, end):
        """Get conversion count for specific view id in daterange
        Args:
            viewid: string, id of specific property
            start: string, startdate in format yyyy-mm-dd
            end: string, enddate in format yyyy-mm-dd
        Returns:
            int, number of goal completions
        """
        obj = self.reporting_API_call(viewid, start, end,
                                      ['goalCompletionsAll'])
        return int(obj['totalsForAllResults']['ga:goalCompletionsAll'])

    def get_total_conversion_count(self, analyticssettings):
        """
        Convenience function to get total of conversions between
        self.GA_NULL_DATE and now
        Args:
            analyticssettings: AnalyticsSettings object containing
            configuration
        Returns:
            total of completed conversions for given configuration
        """
        now = self.google_date(datetime.today())
        viewid = analyticssettings.ga_view
        goalid = analyticssettings.goal_to_track
        return self.get_conversion_count_for_goal(viewid, goalid,
                                                  self.GA_NULL_DATE, now)

    def get_conversion_count_for_goal(self, viewid, goalid, start, end):
        """
        Get conversion count for specific view id and specific goal number
        in daterange
        Args:
            viewid: string, id of specific property
            goalid: id of specific goal
            start: string, startdate in format yyyy-mm-dd
            end: string, enddate in format yyyy-mm-dd
        Returns:
            int, number of goal completions
        """
        action = 'goal{}Completions'.format(goalid)
        obj = self.reporting_API_call(viewid, start, end, [action])
        return int(obj['totalsForAllResults']['ga:'+action])

    def get_conversion_rate_for_goal(self, viewid, goalid, start, end):
        """
        Get conversion rate for specific view id and specific goal number
        in daterange
        Args:
            viewid: string, id of specific property
            goalid: id of specific goal
            start: string, startdate in format yyyy-mm-dd
            end: string, enddate in format yyyy-mm-dd
        Returns:
            perc, goal gonversion rate
        """
        action = 'goal{}ConversionRate'.format(goalid)
        obj = self.reporting_API_call(viewid, start, end, [action])
        return round(float(obj['totalsForAllResults']['ga:'+action]), 2)

    def get_daily_conversions_for_goal(self, viewid, goalid, start, end):
        """
        Get conversion count for given goal in view between start and end,
        sorted by date
        """
        start_str = self.google_date(start)
        end_str = self.google_date(end)
        action = 'goal{}Completions'.format(goalid)
        return self.reporting_API_call(viewid, start_str, end_str, [action],
                                       '&sort=ga:date&dimensions=ga:date')

    def get_conversion_count_summary(self, viewid, start, end):
        """
        Get list of conversion names and corresponding counts in
        given time interval
        """
        return self.reporting_API_call(viewid, start, end,
                                       ['goalCompletionsAll'])

    def get_session_count(self, viewid, start, end):
        """Get session count for specific view id in daterange
        Args:
            viewid: string, id of specific property
            start: string, startdate in format yyyy-mm-dd
            end: string, enddate in format yyyy-mm-dd
        Returns:
            int, number of sessions
        """
        obj = self.reporting_API_call(viewid, start, end, ['sessions'])
        return int(obj['totalsForAllResults']['ga:sessions'])

    def get_referrals(self, viewid, start, end, max_results=30):
        """
        Get listing of full referral dimension (where do they come from?)
        """
        start_str = self.google_date(start)
        end_str = self.google_date(end)
        return self.reporting_API_call(viewid, start_str, end_str, ['sessions'], '&dimensions=ga:fullReferrer&max-results={}&sort=-ga:sessions'.format(max_results))

    def get_channels_for_sessions(self, viewid, start, end):
        """
        Get channel grouping as dimension for sessions
        between start and end
        Args:
            viewid: string, id of specific property
            start: datetime, startdate
            end: datetime, enddate
        Returns:
            channels...
        """
        start_str = self.google_date(start)
        end_str = self.google_date(end)
        return self.reporting_API_call(viewid, start_str, end_str,
                                       ['sessions'],
                                       '&dimensions=ga:channelGrouping')

    def get_device_categories_for_sessions(self, viewid, start, end):
        """
        Get device categories (tablet, mobile or desktop) as dimension
        for sessions between start and end
        Args:
            viewid: string, id of specific property
            start: datetime, startdate
            end: datetime, enddate
        Returns:
            device categories...
        """
        start_str = self.google_date(start)
        end_str = self.google_date(end)
        return self.reporting_API_call(viewid, start_str, end_str,
                                       ['sessions'],
                                       '&dimensions=ga:deviceCategory')

    def get_top_pages(self, viewid, start, end, max_results=5):
        """
        Get list of pages + titles ordered by session count between
        start and end
        https://www.googleapis.com/analytics/v3/data/ga?ids=ga%3A3374369&dimensions=ga%3ApagePath%2Cga%3ApageTitle&metrics=ga%3Asessions&start-date=2014-11-11&end-date=2014-11-25&max-results=50
        """
        start_str = self.google_date(start)
        end_str = self.google_date(end)
        response = self.reporting_API_call(viewid, start_str, end_str,
                                           ['pageViews'],
                                           '&dimensions=ga:pagePath,ga:pageTitle&max-results={}'.format(max_results))
        return response.get('rows')

    def reporting_API_call(self, viewid, start, end, metrics, extra=''):
        """Generic method for API Calls to Reporting API
        Args:
            viewid: string, id of specific property
            start: string, startdate in format yyyy-mm-dd
            end: string, enddate in format yyyy-mm-dd
            metrics: list of strings, metrics to be fetched e.g.
            goalCompletionsAll, sessions
            extra: string to append to the query-url
        Returns:
            json decoded http response
        """
        url = self.GA_REPORTING_URL + 'ids=ga:{}&start-date={}&end-date={}'.format(viewid, start, end)
        url += '&metrics='
        for metric in metrics:
            url += 'ga:{},'.format(metric)
        url = url[:-1]
        url += extra
        return self.API_call(url)

    def API_call(self, url):
        """
        Generic base API interfacing method
        """
        token = self.get_access_token_for_user()
        self.logger.debug('calling url: {}'.format(url))
        response = requests.get(url, params={'access_token': token})
        self.logger.debug('response: {}'.format(response.content))
        return json.loads(response.content)

    def get_access_token_for_user(self, user=None):
        """
        Retrieve social_auth token for given user, fall back to default user if
        none given. This is only for demo/R&D purposes.
        """
        self.logger.debug('get acces token debug test')
        if user is None:
            user = User.objects.get(username=settings.SOCIAL_AUTH_FALLBACK_USERNAME)
        # get the stored oauth2 access token for user
        social = user.social_auth.get(provider='google-oauth2', user=user)
        # get a new access token using the refresh token if necessary
        if social.extra_data['expires'] == 0:
            self.logger.debug("""access token expired, retrieving new token
                              using refresh token""")
            strategy = load_strategy(backend='google-oauth2')
            social.refresh_token(strategy)
        return social.extra_data['access_token']

    """
    Management API functions and utils
    """

    GA_MANAGEMENT_URL = 'https://www.googleapis.com/analytics/v3'

    def get_accounts(self):
        url = '{}/management/accountSummaries'.format(self.GA_MANAGEMENT_URL)
        return self.API_call(url)

    def get_properties(self, account_id):
        url = '{}/management/accounts/{}/webproperties'.format(self.GA_MANAGEMENT_URL, account_id)
        return self.API_call(url)

    def get_profiles(self, account_id, property_id):
        return self.API_call('{}/management/accounts/{}/webproperties/{}/profiles'.format(self.GA_MANAGEMENT_URL, account_id, property_id))

    def reverse_view_lookup(self, view_id):
        accounts = self.get_accounts()
        result = 'not found'
        for account_summary in accounts.get('items'):
            for web_property in account_summary.get('webProperties'):
                for profile in web_property.get('profiles'):
                    if profile.get('id') == view_id:
                        account_id = account_summary.get('id')
                        property_id = web_property.get('id')
                        result = self.API_call('{}/management/accounts/{}/webproperties/{}'.format(self.GA_MANAGEMENT_URL, account_id, property_id))
        return result

    def get_goals_for_view(self, view_id):
        """
        Return list of goals for given view (and account / property )
        see: https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/goals/list
        """
        web_property = self.reverse_view_lookup(view_id)
        account_id = web_property.get('accountId')
        property_id = web_property.get('id')
        url = '{}/management/accounts/{}/webproperties/{}/profiles/{}/goals'.format(self.GA_MANAGEMENT_URL, account_id, property_id, view_id)
        return self.API_call(url)

    """
    Helper and convenience functions
    """
    def google_date(self, date):
        """
        Helper function to convert a datetime object to the format
        Google wants (yyyy-mm-dd)
        """
        return datetime.strftime(date, "%Y-%m-%d")