from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from django.views import generic
from django.core.urlresolvers import reverse
from monitor.models import Project, Summary, BuzzartUpdate
from datetime import date, timedelta, datetime
from niki.nikiconverter import NikiConverter
from nikiInterest import interestmanager
from django.shortcuts import get_object_or_404
from nikiInterest.models import InterestAccount
from googleAnalytics.analyticsmanager import AnalyticsManager
from django.shortcuts import render_to_response
import models
from facebook.fbmanager import FacebookManager
from facebookAds.models import FacebookAdsSettings
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as djlogin, logout as djlogout
from dateutil import parser
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMultiAlternatives
import json
from guardian.shortcuts import get_objects_for_user
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


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


@login_required()
def index(request):
    """
    View for main entrance, listing various possible actions
    in the buzzart application. 
    """    
    
    all_projects = models.Project.objects.all()
    projects = get_objects_for_user(request.user, 'view_project', all_projects)
    
    fbads_settings = FacebookAdsSettings.objects.first()
    return render_to_response('index.html',{
                               'projects': projects,                               
                               'fbads_settings': fbads_settings},
                              context_instance=RequestContext(request))

@login_required()
def set_reporting_date(request):    
    request.session['start'] = request.POST.get('start')
    request.session['end'] = request.POST.get('end')  
    return redirect(request.POST.get('next'))

@user_passes_test(lambda u:u.is_staff, login_url='/login')
def email_update(request, update_id):
    """
    Send the content of a specific Buzzart Update to
    the project owner via email. The mail contains a link to the 
    web version of the dashboard. Only staff members can send these mails.
    After succesfully sending the mail, flag the update as mail_sent = True
    """
    update = BuzzartUpdate.objects.get(id=update_id)
    project = update.project
    subject, from_email, to = update.title, settings.NOTIFIER_FROM_MAIL, project.email
    bcc = settings.NOTIFIER_BCC
    text_content = update.update    
    static_full_url = request.build_absolute_uri(settings.STATIC_URL)
    dashboard_url = request.build_absolute_uri('/dashboard/{}'.format(project.id))    
    #html_content = '<p>{}</p><p>Bekijk je dashboard hier: <a href="{}">{}</a></p>'.format(update.update, dashboard_url, dashboard_url)    
    html_content = render_to_string('update-mailing.html', 
                                    {'update': update, 
                                     'project': project,
                                     'dashboard_url': dashboard_url,
                                     'static_full_url' : static_full_url}, 
                                    context_instance=RequestContext(request))        
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], bcc)
    msg.attach_alternative(html_content, "text/html")
    data = msg.send()
    if data:        
        update.mail_sent = True
        update.save()
        return redirect('/dashboard/{}'.format(project.id))
    else:
        return HttpResponse(json.dumps('Sending mail failed'), content_type='application/json')
    
    
@user_passes_test(lambda u:u.is_staff, login_url='/login')
def preview_update(request, update_id):
    """
    Render the content of a buzzart update in the Buzzart update mail template
    as a method of previewing the contents.
    """
    update = BuzzartUpdate.objects.get(id=update_id)
    project = update.project
    static_full_url = request.build_absolute_uri(settings.STATIC_URL)
    dashboard_url = request.build_absolute_uri('/dashboard/{}'.format(project.id))
    return render_to_response('update-mailing.html', 
                              {'update': update, 
                               'project': project,
                               'dashboard_url': dashboard_url,
                               'static_full_url' : static_full_url  },
                               context_instance=RequestContext(request)
                              )
    
    

@user_passes_test(lambda u:u.is_staff, login_url='/login')
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
