from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, render_to_response
from django.views import generic
from niki.models import Account
from niki.nikiconverter import NikiConverter


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


def project_list(request):
    nc = NikiConverter()
    return render_to_response('niki/projects.html',
                              {"projects": nc.getAllProjects()},
                              content_type="text/html")
