from django.db import models
from monitor.models import BuzzartUpdate
from datetime import datetime, timedelta
from datetime import date
from dashboard import util
import logging
from monitor.models import BuzzCache

class BuzzartManager:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_updates_over_time(self, project, start, end):
        '''
        Get a list of buzzart updates for a given project, formatted
        as highchart flags tuples ({x, title, text})
        '''
        updates = BuzzartUpdate.objects.filter(project = project) \
                                       .filter(posted__range=[start, end])
        
        
        result = []
        for item in updates:             
            dt = datetime.combine(item.posted, datetime.min.time())
            result.append({'x':util.unix_time_millis(dt),
                           'title': 'B',
                           'text': item.title })
        return result
    
class BuzzCacheManager(models.Manager):
    
    def get(self, *args, **kwargs):
        models.Manager.get(self, *args, **kwargs)
            
