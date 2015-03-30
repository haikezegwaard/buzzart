import datetime
from datetime import timedelta
from dateutil import parser
from django.contrib.sessions.backends.db import SessionStore

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
def iso_string_to_milliseconds(isodate):
    """
    Convert ISO formatted date time string to timezone naive 
    milliseconds since Unix EPOCH
    """
    date = parser.parse(isodate)
    nozone = date.replace(tzinfo=None)
    return unix_time_millis(nozone)


def get_reporting_dates(request):
    """
    Date range for all reporting functions
    """
    session = request.session
    date_range = {}    
    if not session.get('start') is None:
        date_range['start'] = parser.parse(session.get('start'))
    else:
        date_range['start'] = datetime.datetime.today() - datetime.timedelta(days=128)

    if not session.get('end') is None:
        date_range['end'] = parser.parse(session.get('end'))
    else:
        date_range['end'] = datetime.datetime.today() - datetime.timedelta(days=1)
    return date_range
    
    
             

