from django.shortcuts import render
from django.http import HttpResponse
from twitter import *

# Create your views here.
def index(request):

    token = '15916075-vCZIeZn3f4ksDz3Qg8RRgk4opE0rqhkOHkSR2GE4x'
    token_key = 'Emoq1PJAn98K2mbjBT6hXkfxpmllMLuxwWFYZpBYOr4eD'
    con_secret = 'nyylZGieWcZYpylxocCGySDv5rcHwgTMXK9MOmeIbjqBbBKigW'
    con_secret_key = 'pfhysTbUY4iTCVpdS3MwXHWPc'



    t = Twitter(auth=OAuth(token, token_key, con_secret, con_secret_key)))
    return HttpResponse('test', mimetype='text/html')
