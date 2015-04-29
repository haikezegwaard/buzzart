from django.shortcuts import render
from django.views import generic
from nikiInterest.models import InterestAccount
from nikiInterest.interestmanager import InterestManager
from datetime import date, datetime, timedelta
import xml.etree.ElementTree as ET
import json
from monitor import models as monitor_models
from django.http import HttpResponse
from dashboard import util

# Create your views here.
# Create your views here.

class IndexView(generic.TemplateView):

    #model = InterestAccount
    template_name = 'nikiInterest/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexView,self).get_context_data(**kwargs)
        start = datetime.today() - timedelta(days=14)
        # Add in a QuerySet of all the books
        interestManager = InterestManager()
        account = InterestAccount.objects.get(username='vanwijnen@fundament.nl')
        context['all'] = interestManager.getIdsByProject(account, 'GEN_630D1B86-31EE-494F-A718-48C8B6B4EA11')
        return context

def subscriptions_total(request, project_id):
    """
    To call using AJAX, perhaps this is too heavy for just a count?
    """
    project = monitor_models.Project.objects.get(id = project_id)
    interestManager = InterestManager()
    count = interestManager.get_count_for_project(project)
    data = {'subscriptions' : count}
    return HttpResponse(json.dumps(data), content_type='application/json')

def subscriptions_per_type(request, project_id):
    """
    List housetypes and according subscriptions in a dictionary
    """
    project = monitor_models.Project.objects.get(id = project_id)
    date_range = util.get_reporting_dates(request)
    start = date_range['start']
    end = date_range['end']
    interestManager = InterestManager()
    count = interestManager.get_count_by_housetype(project, start, end)
    data = []   
    for key, value in count:
        data.append({'woningtype': key, 'interesse': value}) 
    return HttpResponse(json.dumps(data), content_type='application/json')






