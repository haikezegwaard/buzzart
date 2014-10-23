from django.shortcuts import render
import mailchimp
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, loader
import logging
from mailchimp_manager import MailchimpManager
import json
from django.http import HttpResponse
import dateutil.parser
import time

m = MailchimpManager('8e7536a78b89a35edfa0122d2e417186-us1')
# Create your views here.
def index(request):


    list_growth = m.get_list_size_data('23c3cfb062')

    return render_to_response('members.html', {'members' :  list_growth}, context_instance=RequestContext(request))


def chart_data_json(request):
    data = {}
    params = request.GET

    days = params.get('listid', '')
    members = m.get_members('a30a6e97d6')
    cumulative = 0
    data = []
    logger = logging.getLogger(__name__)
    for member in members.get('data'):
        cumulative += 1
        mydate = dateutil.parser.parse(member.get('timestamp_opt'))
        data.append([time.mktime(mydate.timetuple()), cumulative])
    logger.debug(data)
    return HttpResponse(json.dumps(data), content_type='application/json')