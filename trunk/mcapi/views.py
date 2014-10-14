from django.shortcuts import render
import mailchimp
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, loader
import logging
from mailchimp_manager import MailchimpManager
import json
from django.http import HttpResponse

# Create your views here.
mcman = MailchimpManager('8e7536a78b89a35edfa0122d2e417186-us1')

def index(request):
    list_growth = mcman.get_list_size_data('23c3cfb062')
    return render_to_response('list.html', {'list_growth' : list_growth}, context_instance=RequestContext(request))


def list_members(request):
    data = {}
    params = request.GET
    list_id = params.get('listid', '')
    data = mcman.api.lists.members(list_id)
    return HttpResponse(json.dumps(data), content_type='application/json')

