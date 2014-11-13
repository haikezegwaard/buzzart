from django.contrib.auth.models import User
import requests
import logging
import json
from datetime import datetime
from social.apps.django_app.utils import load_strategy
from datetime import timedelta


class AnalyticsManager:

    GA_URL = 'https://www.googleapis.com/analytics/v3/data/ga?'

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
        user = User.objects.get(username="haike") #this should not be static
        #get the oath2 token for user haike
        social = user.social_auth.get(provider='google-oauth2')
        strategy = load_strategy(backend='google-oauth2')
        social.refresh_token(strategy)

        url = self.GA_URL + 'ids=ga:{}&start-date={}&end-date={}'.format(viewid, start, end)
        url += '&metrics='
        for metric in metrics:
            url += 'ga:{},'.format(metric)
        url = url[:-1]
        url += extra
        self.logger.debug('calling url: '+url)
        response = requests.get(url,params={'access_token': social.extra_data['access_token']})

        self.logger.debug('response: '+response.content)
        return json.loads(response.content)


    def google_date(self, date):
        """
        Helper function to convert a datetime object to the format
        Google wants (yyyy-mm-dd)
        """
        return datetime.strftime(date, "%Y-%m-%d")