from django.shortcuts import render
from django.http import HttpResponse
from twitter import *

# Create your views here.
def index(request):

    oauth_token = '15916075-vCZIeZn3f4ksDz3Qg8RRgk4opE0rqhkOHkSR2GE4x'
    oauth_secret = 'Emoq1PJAn98K2mbjBT6hXkfxpmllMLuxwWFYZpBYOr4eD'
    consumer_secret = 'nyylZGieWcZYpylxocCGySDv5rcHwgTMXK9MOmeIbjqBbBKigW'
    consumer_key = 'pfhysTbUY4iTCVpdS3MwXHWPc'



    t = Twitter(auth=OAuth(oauth_token, oauth_secret,
                           consumer_secret, consumer_key))
    return HttpResponse(t.statuses.home_timeline(), mimetype='text/html')
