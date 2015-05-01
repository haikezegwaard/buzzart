import analyticsmanager
import models
from dashboard import util
from dateutil import parser
import logging
from monitor.models import Project
from django.core.exceptions import ObjectDoesNotExist

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
        settings = self.getSettingsByProject(project)
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
        settings = self.getSettingsByProject(project)
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
        settings = self.getSettingsByProject(project)       
        goals = self.ga_manager.get_goals_for_view(settings.ga_view)
        result = []
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
        settings = self.getSettingsByProject(project)
        channels = self.ga_manager.get_channels_for_sessions(settings.ga_view, start, end)
        result = []
        for item in channels.get('rows'):
            result.append([item[0],int(item[1])])
        return result

    def get_device_category_for_sessions(self, project, start, end):
        """
        Get the device for sessions (tablet, mobile, desktop)
        """
        settings = self.getSettingsByProject(project)
        categories = self.ga_manager.get_device_categories_for_sessions(settings.ga_view, start, end)
        result = []
        for item in categories.get('rows'):
            result.append([item[0], int(item[1])])
        return result
    

    def getSettingsByProject(self, project):
        settings = False
        try:
            settings = models.AnalyticsSettings.objects.get(project=project)                    
        except ObjectDoesNotExist:
            self.logger.warn('Analytics settings not found for project: {}'.format(project.name))
        return settings
        
            

    def get_bounce_rate(self, project, start, end):
        """
        Get bounce rate for view in project
        """
        settings = self.getSettingsByProject(project)
        response = self.ga_manager.get_bounce_rate(settings.ga_view, start, end)
        rows = response.get('rows')
        if not len(rows) is 1:
            raise Exception('rows size was not 1 ({})'.format(len(rows)))
        return float(rows[0][0])
    
    def get_avg_session_duration(self, project, start, end):
        """
        Get bounce rate for view in project
        """
        settings = self.getSettingsByProject(project)
        response = self.ga_manager.get_avg_session_duration(settings.ga_view, start, end)
        rows = response.get('rows')
        if not len(rows) is 1:
            raise Exception('rows size was not 1 ({})'.format(len(rows)))        
        return float(rows[0][0])
             
    def get_summary(self, project, start, end):
        """
        Summarize bouncerate, session duration
        """        
        result = []
        bouncerate = self.get_bounce_rate(project, start, end)
        sessionduration = self.get_avg_session_duration(project, start, end)
        overall_bounce = self.get_overall_avg_bounce_rate(start, end)
        overall_session_duration = self.get_overall_avg_session_duration(start, end)
        result.append({'name': 'bouncerate', 'value': round(bouncerate, 2),'average': overall_bounce})        
        result.append({'name': 'time on site', 'value': round(sessionduration, 2), 'average': overall_session_duration})
        return result

    def get_referrals(self, project, start, end):
        """
        Get ordered list of tuples (referral, sessioncount) for given project
        between dates
        """
        settings = self.getSettingsByProject(project)
        referrals = self.ga_manager.get_referrals(settings.ga_view, start, end)
        result = []
        for item in referrals.get('rows'):
            result.append([item[0], int(item[1])])
        return sorted(result, key=lambda tup: tup[1], reverse=True)
    
    def get_overall_avg_bounce_rate(self, start, end):
        """
        Get the overall average ('branche average') bouncerate 
        between start and en date
        """
        # first check for 'cache' hit
        
        # no hit, calculate new value
        projects = Project.objects.all()
        avgs = []
        for project in projects:
            try:
                br = self.get_bounce_rate(project, start, end)
            except:
                br = None
            if br is not None:
                avgs.append(br)
        if len(avgs) > 0:
            avg_bounce_rate = round(sum(avgs) / len(avgs), 2)
            # store value in db
        else:
            return 0
    
    def get_overall_avg_session_duration(self, start, end):
        """
        Get the overall average ('branche average') session duration 
        between start and en date
        """
        projects = Project.objects.all()
        avgs = []
        for project in projects:
            try:
                sd = self.get_avg_session_duration(project, start, end)
            except:
                sd = None
            if sd is not None:
                avgs.append(sd)
        if len(avgs) > 0:
            return round(sum(avgs) / len(avgs), 2)
        else:
            return None

