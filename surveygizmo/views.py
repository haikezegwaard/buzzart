'''
Created on Mar 27, 2015

@author: hz
'''
import requests
from surveygizmo_manager import SurveyGizmoManager
from monitor.models import Project
from django.http import HttpResponse
import json

manager = SurveyGizmoManager()

def get_survey(request, project_id):
    project = Project.objects.get(id = project_id)
    result = manager.get_survey(project)
    return HttpResponse(json.dumps(result), content_type='application/json')

def get_survey_statistics(request, project_id):
    project = Project.objects.get(id = project_id)
    result = manager.get_survey_statistics(project)
    return HttpResponse(json.dumps(result), content_type='application/json')

def get_survey_report(request, project_id):
    project = Project.objects.get(id = project_id)
    result = manager.get_survey_report(project)
    return HttpResponse(json.dumps(result), content_type='application/json')