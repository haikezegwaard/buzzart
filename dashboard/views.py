from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import json
from datetime import timedelta
import datetime
import random
from mcapi.mailchimp_manager import MailchimpManager
import util
from monitor.models import Project
from dateutil import parser
from googleAnalytics.analyticsmanager import AnalyticsManager
from googleAnalytics.models import AnalyticsSettings
from nikiInterest.interestmanager import InterestManager
from nikiInterest.models import InterestAccount
from monitor.models import InterestProject, BuzzartUpdate
from nikiInterest import statsservice
from googleAnalytics import statsservice as googlestats
from mcapi import statsservice as mcstats
import logging
from django.contrib.sessions.backends.db import SessionStore
from googleAnalytics import helper
from forms import UpdateForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

session = SessionStore()

logger = logging.getLogger(__name__)

# Create your views here.
def index(request, project_id):
    project = Project.objects.get(id=project_id)
    if not request.GET.get('start') is None:
        session['start'] = parser.parse(request.GET.get('start'))
    if not request.GET.get('end') is None:
        session['end'] = parser.parse(request.GET.get('end'))

    template = request.GET.get('template', '')
    account = ''
    if template:
        account = template + '/'

    return render_to_response(account+'home.html',
                              {'project_id': project_id,
                               'project': project,
                               'campaigns': get_campaigns(project_id),
                               'traffic': get_google_stats(project_id),
                               'subscribers': get_subscriptions(project_id),
                               'updates': get_updates(project_id),
                               'start': datetime.date.strftime(get_start(),"%m/%d/%Y"),
                               'end': datetime.date.strftime(get_end(),"%m/%d/%Y")
                               },
                              context_instance=RequestContext(request))


def origin(request, project_id):
    template = request.GET.get('template', '')
    account = ''
    if template:
        account = template + '/'
    project = Project.objects.get(id=project_id)
    return render_to_response(account+'origin.html',
                              {'project_id': project_id,
                               'project': project,
                               'updates': get_updates(project.id),
                               'referrals':get_referrals(project_id)
                               },
                              context_instance=RequestContext(request))


def profiles(request, project_id):
    template = request.GET.get('template', '')
    account = ''
    if template:
        account = template + '/'
    project = Project.objects.get(id=project_id)
    return render_to_response(account+'profiles.html',
                              {
                               'project': project
                               },
                              context_instance=RequestContext(request))


def adwords(request, project_id):
    template = request.GET.get('template', '')
    account = ''
    if template:
        account = template + '/'
    project = Project.objects.get(id=project_id)
    return render_to_response(account+'adwords.html',
                              {
                               'project': project
                               },
                              context_instance=RequestContext(request))


def fbads(request, project_id):
    template = request.GET.get('template', '')
    account = ''
    if template:
        account = template + '/'
    project = Project.objects.get(id=project_id)
    return render_to_response(account+'fbads.html',
                              {
                               'project': project
                               },
                              context_instance=RequestContext(request))


def mailing(request, project_id):
    template = request.GET.get('template', '')
    account = ''
    if template:
        account = template + '/'
    project = Project.objects.get(id=project_id)
    return render_to_response(account+'mailing.html',
                              {
                               'project': project
                               },
                              context_instance=RequestContext(request))


def site_list(request):
    template = request.GET.get('template', '')
    account = ''
    if template:
        account = template + '/'
    return render_to_response(account+'corporate/sitelist.html',
                              {},
                              context_instance=RequestContext(request))


def corporate_updates(request):
    return render_to_response('corporate/updates.html',
                              {},
                              context_instance=RequestContext(request))

def compose_update(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form =  UpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/{}'.format(project_id))
    else:
        data = { 'project': project,
                 'posted': datetime.datetime.now()
               }
        form = UpdateForm(initial= data)
    return render(request, 'updates/compose-update.html',
                  {'form': form,
                   'project': project})

def project_updates(request, project_id):
    project = Project.objects.get(id=project_id)
    return render_to_response('timeline.html',
                              {'project': project,
                               'updates': get_updates(project.id)},
                              context_instance=RequestContext(request))


def get_updates(project_id):
    project = Project.objects.get(id=project_id)
    updates = BuzzartUpdate.objects.filter(project=project)
    return updates


ga_stats = googlestats.StatsService()


def get_start():
    if not session.get('start') is None:
        return session.get('start')
    else:
        return datetime.datetime.today() - datetime.timedelta(days=128)


def get_end():
    if not session.get('end') is None:
        return session.get('end')
    else:
        return datetime.datetime.today() - datetime.timedelta(days=1)

start = get_start()
end = get_end()


def get_referrals(project_id):
    project = Project.objects.get(id=project_id)
    return ga_stats.get_referrals(project, start, end)


def get_google_stats(project_id):
    project = Project.objects.get(id=project_id)
    try:
        return ga_stats.get_traffic_over_time(project, start, end)
    except:
        logger.error('could not fetch ga traffic')
        return None


def get_campaigns(project_id):
    project = Project.objects.get(id=project_id)
    if project.mailchimp_list_id == '0': return None
    mc_stats = mcstats.StatsService()
    result = mc_stats.get_campaigns_over_time(project, start, end)
    return result



def get_subscriptions(project_id):
    """
    Get Niki subcribers for given project, returns a list of
    tuples (stamp, count) for the use of plotting in a graph
    """
    # project = Project.objects.get(id=project_id)
    stats_service = statsservice.StatsService()
    # return stats_service.get_subscriptions_over_time(project, start_date, end_date)
    return stats_service.get_mock_subscriptions()


def get_conversions(project_id):
    project = Project.objects.get(id=project_id)
    return ga_stats.get_conversions_over_time(project, start, end)


def plottingDataSeries(request, project_id):
    traffic = []
    subscriptions = []
    for single_date in util.daterange(start, end):
        traffic.append([util.unix_time_millis(single_date),random.randint(50, 150)])
        subscriptions.append([util.unix_time_millis(single_date),random.randint(0, 2)])

    data = [{"name": "data1", "data": get_google_stats(project_id)},
            {"name": "data2", "data": get_conversions(project_id)},
            {"name": "data3", "data": get_campaigns(project_id)},
            # {"name": "data4", "data": get_subscriptions(project_id)}]
            {"name": "data4", "data": subscriptions}]
    return HttpResponse(json.dumps(data), content_type='application/json')
