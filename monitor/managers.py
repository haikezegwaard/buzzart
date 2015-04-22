from django.db import models
from monitor.models import BuzzartUpdate
from datetime import datetime
from datetime import date
from dashboard import util

class BuzzartManager:
    
    def get_updates_over_time(self, project, start, end):
        '''
        Get a list of buzzart updates for a given project, formatted
        as highchart flags tuples ({x, title, text})
        '''
        updates = BuzzartUpdate.objects.filter(project = project)
        result = []
        for item in updates:             
            dt = datetime.combine(item.posted, datetime.min.time())
            result.append({'x':util.unix_time_millis(dt),
                           'title': 'B',
                           'text': item.title })
        return result
