import analyticsmanager
import models
from dashboard import util
from dateutil import parser

class StatsService():
    """
    Class for converting Niki Interest data to graph/plotting format
    Target format is (mostly) list of tuples: [(timestamp,count)]
    """

    def __init__(self):
        self.ga_manager = analyticsmanager.AnalyticsManager()

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