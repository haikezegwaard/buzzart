from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import json
from datetime import timedelta
import datetime
import random
import util


# Create your views here.
def index(request):
    return render_to_response('home.html',{'foo':'bar'},context_instance=RequestContext(request))


def mockDualSeries(request):
    traffic = []
    subscriptions = []
    start_date = datetime.datetime.today() - datetime.timedelta(days = 31)
    end_date = datetime.datetime.today()
    for single_date in util.daterange(start_date, end_date):
        traffic.append([util.unix_time_millis(single_date),random.randint(50,150)])
        subscriptions.append([util.unix_time_millis(single_date),random.randint(0,2)])

    data = [{"name":"data1", "data": traffic},
            {"name":"data2", "data":subscriptions}]
    return HttpResponse(json.dumps(data), content_type='application/json')

