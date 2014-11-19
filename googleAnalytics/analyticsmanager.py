from django.contrib.auth.models import User
import requests
import logging
import json
from datetime import datetime
from social.apps.django_app.utils import load_strategy
from datetime import timedelta


class AnalyticsManager:

    GA_REPORTING_URL = 'https://www.googleapis.com/analytics/v3/data/ga?'

    logger = logging.getLogger(__name__)

    GA_NULL_DATE = '2005-01-01'

    def get_weekly_visits(self, viewid, start, end):
        """For convenience only"""
        return self.reporting_API_call(viewid, start, end, ['sessions','pageviews'], '&sort=ga:date&dimensions=ga:date&max-results=200')

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
        return self.reporting_API_call(viewid, start_str, end_str, ['sessions'], '&sort=ga:date&dimensions=ga:date')

    def get_conversion_count(self, viewid, start, end):
        """Get conversion count for specific view id in daterange
        Args:
            viewid: string, id of specific property
            start: string, startdate in format yyyy-mm-dd
            end: string, enddate in format yyyy-mm-dd
        Returns:
            int, number of goal completions
        """
        obj = self.reporting_API_call(viewid, start, end, ['goalCompletionsAll'])
        return int(obj['totalsForAllResults']['ga:goalCompletionsAll'])

    def get_total_conversion_count(self, analyticssettings):
        """
        Convenience function to get total of conversions between
        self.GA_NULL_DATE and now
        Args:
            analyticssettings: AnalyticsSettings object containing configuration
        Returns:
            total of completed conversions for given configuration
        """
        now = self.google_date(datetime.today())
        viewid = analyticssettings.ga_view
        goalid = analyticssettings.goal_to_track
        return self.get_conversion_count_for_goal(viewid, goalid, self.GA_NULL_DATE, now)

    def get_conversion_count_for_goal(self, viewid, goalid, start, end):
        """Get conversion count for specific view id and specific goal number in daterange
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
        """Get conversion rate for specific view id and specific goal number in daterange
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
        return round(float(obj['totalsForAllResults']['ga:'+action]),2)

    def get_daily_conversions_for_goal(self, viewid, goalid, start, end):
        """
        Get conversion count for given goal in view between start and end,
        sorted by date
        """
        start_str = self.google_date(start)
        end_str = self.google_date(end)
        action = 'goal{}Completions'.format(goalid)
        return self.reporting_API_call(viewid, start_str, end_str, [action], '&sort=ga:date&dimensions=ga:date')

    def get_conversion_count_summary(self, viewid, start, end):
        """
        Get list of conversion names and corresponding counts in
        given time interval
        """
        start_str = self.google_date(start)
        end_str = self.google_date(end)
        obj = self.reporting_API_call(viewid, start, end, ['goalCompletionsAll'])
        return obj

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

    def get_referrals(self, viewid, start, end):
        """
        Get listing of full referral dimension (where do they come from?)
        """
        start_str = self.google_date(start)
        end_str = self.google_date(end)
        return self.reporting_API_call(viewid, start_str, end_str, ['sessions'], '&dimensions=ga:fullReferrer')

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
        return self.reporting_API_call(viewid, start_str, end_str, ['sessions'], '&dimensions=ga:channelGrouping')


    def reporting_API_call(self, viewid, start, end, metrics, extra = ''):
        """Generic method for API Calls to Reporting API
        Args:
            viewid: string, id of specific property
            start: string, startdate in format yyyy-mm-dd
            end: string, enddate in format yyyy-mm-dd
            metrics: list of strings, metrics to be fetched e.g. goalCompletionsAll, sessions
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
        user = User.objects.get(username="haike") #this should not be static
        #get the oath2 token for user haike
        social = user.social_auth.get(provider='google-oauth2')
        strategy = load_strategy(backend='google-oauth2')
        social.refresh_token(strategy)
        self.logger.debug('calling url: {}'.format(url))
        response = requests.get(url,params={'access_token': social.extra_data['access_token']})
        self.logger.debug('response: {}'.format(response.content))
        return json.loads(response.content)

    """
    Management API functions and utils
    """

    GA_MANAGEMENT_URL = 'https://www.googleapis.com/analytics/v3'

    def get_accounts(self):
        return self.API_call('{}/management/accountSummaries'.format(self.GA_MANAGEMENT_URL))

    def get_properties(self, account_id):
        return self.API_call('{}/management/accounts/{}/webproperties'.format(self.GA_MANAGEMENT_URL, account_id))

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