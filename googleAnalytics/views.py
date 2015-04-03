from django.shortcuts import render_to_response
from django.template import RequestContext
from monitor import models
import models as ga_models
import analyticsmanager
from django.http import HttpResponse
import json
from datetime import datetime as dt
import datetime
import statsservice
from django.shortcuts import redirect
import helper
from dateutil import parser
from dashboard import util


ga_man = analyticsmanager.AnalyticsManager()
ga_stats = statsservice.StatsService()

# Create your views here.
def index(request):
    """
    This is useless
    """
    bar = 3
    return render_to_response('template.html', {'foo' : bar}, context_instance=RequestContext(request))


def conversions_total(request, project_id):
    """
    For AJAX-ing purpose
    """
    settings = helper.get_settings_by_project_id(project_id)
    if not request.GET.get('goalId'):
        data = {'conversions' : ga_man.get_total_conversion_count(settings)}
    else: 
        goalid = request.GET.get('goalId')
        drange = util.get_reporting_dates(request)
        start = drange['start']
        end = drange['end']        
        data = {'conversions' : ga_man.get_conversion_count_for_goal(settings.ga_view, goalid, start, end)}   
    return HttpResponse(json.dumps(data), content_type='application/json')

def bounce_rate(request, project_id):
    """
    Get bounce rate for analytics view in project
    """
    drange = util.get_reporting_dates(request)
    start = drange['start']
    end = drange['end']
    project = models.Project.objects.get(id = project_id)
    data = ga_stats.get_bounce_rate(project, start, end)
    return HttpResponse(json.dumps(data), content_type='application/json')
    

def conversions_daily(request, project_id):
    drange = util.get_reporting_dates(request)
    start = drange['start']
    end = drange['end']    
    settings = helper.get_settings_by_project_id(project_id)
    data = {'conversions' : ga_man.get_daily_conversions_for_goal(settings.ga_view, settings.goal_to_track, start, end)}
    return HttpResponse(json.dumps(data), content_type='application/json')

def channel_info(request, project_id):
    project = models.Project.objects.get(id = project_id)
    drange = util.get_reporting_dates(request)
    start = drange['start']
    end = drange['end']
    result = ga_stats.get_channels_for_sessions(project, start, end)
    return HttpResponse(json.dumps(result), content_type='application/json')

def device_category(request, project_id):
    project = models.Project.objects.get(id = project_id)
    drange = util.get_reporting_dates(request)
    start = drange['start']
    end = drange['end']    
    result = ga_stats.get_device_category_for_sessions(project, start, end)
    return HttpResponse(json.dumps(result), content_type='application/json')

def traffic_this_week(request, project_id):
    end = dt.today()
    start = end - datetime.timedelta(days = 7)
    settings = helper.get_settings_by_project_id(project_id)
    count = ga_man.get_session_count(settings.ga_view, ga_man.google_date(start), ga_man.google_date(end))
    data = {'traffic': count}
    return HttpResponse(json.dumps(data), content_type='application/json')

def traffic(request, project_id):
    drange = util.get_reporting_dates(request)
    start = drange['start']
    end = drange['end']
    settings = helper.get_settings_by_project_id(project_id)
    count = ga_man.get_session_count(settings.ga_view, ga_man.google_date(start), ga_man.google_date(end))
    data = {'traffic': count}
    return HttpResponse(json.dumps(data), content_type='application/json')

def top_pages(request, project_id):
    drange = util.get_reporting_dates(request)
    start = drange['start']
    end = drange['end']
    settings = helper.get_settings_by_project_id(project_id)
    response = ga_man.get_top_pages(settings.ga_view, start, end)
    data = {'pages': response}
    return HttpResponse(json.dumps(data), content_type='application/json')

def conversion_list(request, project_id):
    project = models.Project.objects.get(id=project_id)
    drange = util.get_reporting_dates(request)
    start = drange['start']
    end = drange['end']
    data = ga_stats.get_named_conversion_count(project, start, end)
    return HttpResponse(json.dumps(data), content_type='application/json')  

def summary(request, project_id):
    """
    Summarize Analytics stats to render in a table for example
    """
    project = models.Project.objects.get(id=project_id)
    drange = util.get_reporting_dates(request)
    start = drange['start']
    end = drange['end']
    data = ga_stats.get_summary(project, start, end)
    return HttpResponse(json.dumps(data), content_type='application/json')
     

def list_accounts(request):
    """
    Render a list of all accounts available for user
    """
    data = ga_man.get_accounts()
    return HttpResponse(json.dumps(data), content_type='application/json')

def list_properties(request, account_id):
    data = ga_man.get_properties(account_id)
    return HttpResponse(json.dumps(data), content_type='application/json')

def list_profiles(request, account_id, property_id):
    data = ga_man.get_profiles(account_id, property_id)
    return HttpResponse(json.dumps(data), content_type='application/json')

def find_account(request, profile_id):
    data = ga_man.reverse_view_lookup(profile_id)
    return HttpResponse(json.dumps(data), content_type='application/json')

def list_goals(request, profile_id):
    data = ga_man.get_goals_for_view(profile_id)
    return HttpResponse(json.dumps(data), content_type='application/json')

def redirect_if_no_refresh_token(backend, response, social, *args, **kwargs):
    if backend.name == 'google-oauth2' and social and \
       response.get('refresh_token') is None and \
       social.extra_data.get('refresh_token') is None:
        return redirect('/login/google-oauth2?approval_prompt=force')
