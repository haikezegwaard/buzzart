from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, render_to_response
from django.views import generic
from niki.models import Account
from monitor.models import Project
from niki.nikiconverter import NikiConverter
import json


# Create your views here.

class IndexView(generic.DetailView):
    model = Account
    template_name = 'niki/index.html'
    nikiconverter = NikiConverter()

    def get_object(self):
        account = Account()
        account.username = 'username'
        account.password = 'password'
        self.nikiconverter.getAvailability("/projects/54/AMVP9518")
        account.oauth_token = self.nikiconverter.getProject("/projects/54/AMVP9518")
        return account

nc = NikiConverter()

def project_list(request):
    return render_to_response('niki/projects.html',
                              {"projects": nc.getAllProjects()},
                              content_type="text/html")

def availability(request, project_id):
    project = Project.objects.get(id=project_id)
    av = nc.getLabeledAvailability(project.nikiProject)
    result = [(k,v) for k,v in av.iteritems()]
    return HttpResponse(json.dumps(result), content_type='application/json')

def apicall(request):
    resource = request.GET['resource']
    result = nc.apiRequest(resource)
    return HttpResponse(json.dumps(result), content_type='application/json')
    
