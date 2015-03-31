import analyticsmanager
import models
from dashboard import util
from dateutil import parser
import logging

class StatsService():
    """
    Class for converting Niki Interest data to graph/plotting format
    Target format is (mostly) list of tuples: [(timestamp,count)]
    """

    def __init__(self):
        self.ga_manager = analyticsmanager.AnalyticsManager()
        self.logger = logging.getLogger(__name__)

    def get_traffic_over_time(self, project, start, end):
        """
        Get traffic per day over given interval, format traffic as list of
        tuples (timestamp, traffic-count)
        """
        settings = models.AnalyticsSettings.objects.get(project = project)
        traffic = self.ga_manager.get_daily_visits(settings.ga_view, start, end)
        result = []
        for item in traffic.get('rows'):
            ms = util.unix_time_millis(parser.parse(item[0]))
            count = int(item[1])
            result.append([ms, count])
        return result

    def get_conversions_over_time(self, project, start, end):
        """
        Get conversion count per day over given interval, format traffic as list of
        tuples (timestamp, traffic-count)
        """
        settings = models.AnalyticsSettings.objects.get(project = project)
        conversion = self.ga_manager.get_daily_conversions_for_goal(settings.ga_view, settings.goal_to_track, start, end)
        self.logger.debug(conversion)
        result = []
        for item in conversion.get('rows'):
            ms = util.unix_time_millis(parser.parse(item[0]))
            count = int(item[1])
            result.append([ms, count])
        return result
    
    def get_named_conversion_count(self, project, start, end):
        """
        Get list of tuples (goalname, count) for project over time
        """
        settings = models.AnalyticsSettings.objects.get(project = project)       
        goals = self.ga_manager.get_goals_for_view(settings.ga_view)
        result = []
        start_date = self.ga_manager.google_date(start)
        end_date = self.ga_manager.google_date(end)
        for goal in goals.get('items'):
            goal_id = int(goal.get('id'))
            count = self.ga_manager.get_conversion_count_for_goal(settings.ga_view, 
                                                                  goal_id, 
                                                                  start, 
                                                                  end)
            result.append({'name': goal.get('name'), 'count': count})
        return result

    def get_channels_for_sessions(self, project, start, end):
        """
        Get sessions per channel (Direct, Social, Email, Organic, Referral)
        for the use of plotting in a pie chart
        """
        settings = models.AnalyticsSettings.objects.get(project = project)
        channels = self.ga_manager.get_channels_for_sessions(settings.ga_view, start, end)
        result = []
        for item in channels.get('rows'):
            result.append([item[0],int(item[1])])
        return result

    def get_device_category_for_sessions(self, project, start, end):
        """
        Get the device for sessions (tablet, mobile, desktop)
        """
        settings = models.AnalyticsSettings.objects.get(project = project)
        categories = self.ga_manager.get_device_categories_for_sessions(settings.ga_view, start, end)
        result = []
        for item in categories.get('rows'):
            result.append([item[0], int(item[1])])
        return result
    
    def get_bounce_rate(self, project, start, end):
        """
        Get bounce rate for view in project
        """
        settings = models.AnalyticsSettings.objects.get(project = project)
        response = self.ga_manager.get_bounce_rate(settings.ga_view, start, end)
        rows = response.get('rows')
        if not len(rows) is 1:
            raise Exception('rows size was not 1 ({})'.format(len(rows)))        
        return float(rows[0][0])
             

    def get_referrals(self, project, start, end):
        """
        Get ordered list of tuples (referral, sessioncount) for given project
        between dates
        """
        settings = models.AnalyticsSettings.objects.get(project = project)
        referrals = self.ga_manager.get_referrals(settings.ga_view, start, end)
        result = []
        for item in referrals.get('rows'):
            result.append([item[0], int(item[1])])
        return sorted(result, key=lambda tup: tup[1], reverse=True)


