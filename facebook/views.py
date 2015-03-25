from django.shortcuts import render
from fbmanager import FacebookManager
from monitor.models import Project
from django.http import HttpResponse
import json
from dateutil import parser
from datetime import datetime

# Create your views here.
fbmanager = FacebookManager()

def dateranges(request):
    end = parser.parse(request.session.get('end'))
    if not end:
        end = datetime.today()    
    start = parser.parse(request.session.get('start'))    
    if not start:
        start = end - datetime.timedelta(days = 31)
    s = datetime.strftime(start, "%Y-%m-%d")
    e = datetime.strftime(end, "%Y-%m-%d")
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
    data = [{"name": "data1", "data": fbmanager.get_page_impressions(project, True, True)},
            {"name": "data2", "data": fbmanager.get_page_engaged(project, True, True)},
            {"name": "data3", "data": fbmanager.get_page_fans(project, True, True)}            
            ]
    return HttpResponse(json.dumps(data), content_type='application/json')