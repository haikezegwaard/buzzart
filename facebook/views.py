from django.shortcuts import render
from fbmanager import FacebookManager
from monitor.models import Project
from django.http import HttpResponse
import json

# Create your views here.
PAGE = '217907011622497' #static for now
fbmanager = FacebookManager()
def fanpage_age_sex(request):
    result = fbmanager.get_likes_sex_age(PAGE)
    return HttpResponse(json.dumps(result))


def fanpage_impressions(request, project_id):
    project = Project.objects.get(id = project_id)
    result = fbmanager.get_page_impressions(project)
    return HttpResponse(json.dumps(result))

def fanpage_overview(request, project_id):
    project = Project.objects.get(id = project_id)
    result = fbmanager.get_page_overview(project, True, True)
    return HttpResponse(json.dumps(result))