from django.shortcuts import render
from fbmanager import FacebookManager
from monitor.models import Project
from django.http import HttpResponse
import json
from dateutil import parser


# Create your views here.
fbmanager = FacebookManager()

def fanpage_age_sex(request, project_id):
    project = Project.objects.get(id = project_id)
    result = fbmanager.get_likes_sex_age(project)
    return HttpResponse(json.dumps(result), content_type='application/json')


def fanpage_impressions(request, project_id):
    start_str = request.GET.get('start')
    end_str = request.GET.get('end')
    start =  parser.parse(start_str)
    end = parser.parse(end_str)
    project = Project.objects.get(id = project_id)
    result = fbmanager.get_page_impressions(project, start, end)
    return HttpResponse(json.dumps(result), content_type='application/json')

def fanpage_impressions_by_city(request, project_id):
    project = Project.objects.get(id = project_id)
    result = fbmanager.get_page_impressions_by_city(project, True, True)
    return HttpResponse(json.dumps(result), content_type='application/json')

def fanpage_overview(request, project_id):
    project = Project.objects.get(id = project_id)    
    data = [{"name": "data1", "data": fbmanager.get_page_impressions(project, True, True)},
            {"name": "data2", "data": fbmanager.get_page_engaged(project, True, True)},
            {"name": "data3", "data": fbmanager.get_page_fans(project, True, True)}            
            ]
    return HttpResponse(json.dumps(data), content_type='application/json')