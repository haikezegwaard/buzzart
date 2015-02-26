from django import template
from googleAnalytics import helper as ga_helper
from googleAnalytics.analyticsmanager import AnalyticsManager
import logging


register = template.Library()
logger = logging.getLogger(__name__)

#temp dummy data
#goals = [('goal1',3),('goal2',5)]

def conversion_table(project_id):
    view_id = ga_helper.get_view_by_project_id(project_id)
    ga_manager = AnalyticsManager()
    goals = ga_manager.get_goals_for_view(view_id)
    result = []
    for goal in goals.get('items'):
        goal_id = int(goal.get('id'))
        count = ga_manager.get_total_conversion_count_for_goal(view_id, goal_id)
        result.append((goal.get('name'), count))
    return {'conversions':result}

register.inclusion_tag('widgets/ga-conversion-table.html')(conversion_table)