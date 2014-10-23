from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import json
from datetime import timedelta
import datetime
import random
from mcapi.mailchimp_manager import MailchimpManager
import util
from monitor.models import Project
from dateutil import parser


# Create your views here.
def index(request, project_id):

    return render_to_response('home.html',{'project_id':project_id,'campaigns':get_campaigns(project_id)},context_instance=RequestContext(request))


def get_campaigns(project_id):
    project = Project.objects.get(id = project_id)
    mc_man = MailchimpManager(project.mailchimp_api_token)
    start_date = datetime.datetime.today() - datetime.timedelta(days = 31)
    end_date = datetime.datetime.today()
    start_str = datetime.datetime.strftime(start_date,'%Y-%m-%d %H:%M:%S')
    end_str = datetime.datetime.strftime(end_date,'%Y-%m-%d %H:%M:%S')
    json = mc_man.get_campaigns(start_str,end_str)
    result = []
    for item in json.get('data'):
        if(item.get('status') == 'sent'):
            dt = parser.parse(item.get('send_time'))
            result.append({'x':util.unix_time_millis(dt),'title': 'Mailing verstuurd', 'text':'Mailchimp campaign verstuurd:<br /><b>{}</b>'.format(item.get('title'))})
    return result

def mockDualSeries(request):
    traffic = []
    subscriptions = []
    start_date = datetime.datetime.today() - datetime.timedelta(days = 31)
    end_date = datetime.datetime.today()
    for single_date in util.daterange(start_date, end_date):
        traffic.append([util.unix_time_millis(single_date),random.randint(50,150)])
        subscriptions.append([util.unix_time_millis(single_date),random.randint(0,2)])

    data = [{"name":"data1", "data": traffic},
            {"name":"data2", "data":subscriptions},
            {"name":"data3", "data":get_campaigns(1)}]
    return HttpResponse(json.dumps(data), content_type='application/json')

