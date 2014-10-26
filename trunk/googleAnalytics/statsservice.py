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


