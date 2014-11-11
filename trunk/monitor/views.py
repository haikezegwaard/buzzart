from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse
from monitor.models import Project, Summary
from datetime import date, timedelta, datetime
from niki.nikiconverter import NikiConverter
from nikiInterest import interestmanager
from django.shortcuts import get_object_or_404
from nikiInterest.models import InterestAccount
from googleAnalytics.analyticsmanager import AnalyticsManager
from django.shortcuts import render_to_response
import models
from facebook.fbmanager import FacebookManager


class ProjectDetail(generic.DetailView):
    model = Project
    template_name = 'project.html'


class ProjectSummaryMail(generic.ListView):
    """
    create a new summary, store it and render result
    """
    model = Summary
    template_name = 'summaryList.html'


class ProfileView(generic.TemplateView):

    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProfileView, self).get_context_data(**kwargs)
        analyticsManager = AnalyticsManager()
        context['ga'] = analyticsManager.get_conversion_count('67007798', '2013-01-01', '2014-08-13')
        return context


def index(request):
    """
    View for main entrance, listing various possible actions
    in the buzzart application. For convenience only
    """
    summaries = models.Summary.objects.all()
    return render_to_response('index.html',
                              {'summaries': summaries},
                              context_instance=RequestContext(request))


def facebook_tokens(request):
    """
    List projects and facebook ids / tokens
    retrieve access token per project
    """
    fbmanager = FacebookManager()
    projects = Project.objects.all().exclude(fanpage_id='0')
    for project in projects:
        if project.fanpage_token in ('', '0'):
            token = fbmanager.get_access_token_token(project.fanpage_id)
            project.fanpage_token = token
            project.save()
    return render_to_response('fbtokens.html',
                              {'projects': projects},
                              context_instance=RequestContext(request))
