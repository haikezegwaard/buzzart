from django.shortcuts import render
from fbmanager import FacebookManager
from monitor.models import Project
from django.http import HttpResponse
import json
from dateutil import parser
from datetime import datetime
from dashboard import util
# Create your views here.
fbmanager = FacebookManager()

def dateranges(request):
    date_range = util.get_reporting_dates(request)
    s = datetime.strftime(date_range.get('start'), "%Y-%m-%d")
    e = datetime.strftime(date_range.get('end'), "%Y-%m-%d")
    return {'start': s, 'end':  e}

def fanpage_age_sex(request, project_id):
    project = Project.objects.get(id = project_id)
    result = fbmanager.get_likes_sex_age(project)
    return HttpResponse(json.dumps(result), content_type='application/json')


def fanpage_impressions(request, project_id):
    project = Project.objects.get(id = project_id)
    drange = dateranges(request)
    result = fbmanager.get_page_impressions(project, 
                                            drange.get('start'), 
                                            drange.get('end'))    
    return HttpResponse(json.dumps(result), content_type='application/json')

def fanpage_impressions_by_city(request, project_id):
    drange = dateranges(request)
    project = Project.objects.get(id = project_id)
    result = fbmanager.get_page_impressions_by_city(project, 
                                                    drange.get('start'), 
                                                    drange.get('end'))
    transformed = []
    for key, value in result[0][1].items():
        
        transformed.append({'city': key, 'count': value})
    return HttpResponse(json.dumps(transformed), content_type='application/json')

def fanpage_overview(request, project_id):
    project = Project.objects.get(id = project_id)    
    drange = dateranges(request)
    start = drange.get('start')
    end = drange.get('end')
    data = [{"name": "impressions", "data": fbmanager.get_page_impressions(project, start, end)},
            {"name": "engagement", "data": fbmanager.get_page_engaged(project, start, end)},
            {"name": "fans", "data": fbmanager.get_page_fans(project, start, end)}            
            ]
    return HttpResponse(json.dumps(data), content_type='application/json')