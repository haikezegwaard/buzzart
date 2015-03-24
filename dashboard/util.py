import datetime
from datetime import timedelta
from dateutil import parser

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
    
             

