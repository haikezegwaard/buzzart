from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpRequest
from niki.nikiconverter import NikiConverter
from nikiInterest.interestmanager import InterestManager
from monitor.models import InterestProject
from notifier import util
from datetime import datetime, timedelta
import logging
import json
from collections import Counter
import time
from mcapi.mailchimp_manager import MailchimpManager

logger = logging.getLogger(__name__)


def nikisalecount(request):
    """
    Return sale status of project in cyfe data format
    """
    project = request.GET.get('project')
    nikimanager = NikiConverter()
    availability = nikimanager.getAvailability(project)
    result = "Te koop, Optie, Verkocht\n"
    result += ",".join([str(i) for i in availability])+"\n"
    result += "Color,#00cb13,#ff7f00,#ee0000"
    return HttpResponse(result)


def nikirentcount(request):
    """
    Return rent status of project in cyfe data format
    """
    project = request.GET.get('project')
    nikimanager = NikiConverter()
    availability = nikimanager.getAvailability(project)
    result = "Te huur, Optie, Verhuurd\n"
    result += ",".join([str(i) for i in availability])+"\n"
    result += "Color,#00cb13,#ff7f00,#ee0000"
    return HttpResponse(result)


def nikisaletable(request):
    """
    Return list of housetypes with according sale status
    """
    project = request.GET.get('project')
    nikimanager = NikiConverter()
    housetypes = nikimanager.getHouseTypes(project)
    result = "Woningtype,te koop, in optie, verkocht\n"
    for housetype in housetypes:
        typename = housetype.get('name').replace(',', '&#44;')
        sale = housetype.get('houses').get('for-sale') if housetype.get('houses').get('for-sale') else 0
        option = housetype.get('houses').get('option') if housetype.get('houses').get('option') else 0
        sold = housetype.get('houses').get('sold') if housetype.get('houses').get('sold') else 0
        result += '{},{},{},{}\n'.format(typename, sale, option, sold)
    return HttpResponse(result)


def nikirenttable(request):
    """
    Return list of housetypes with according rent status
    """
    project = request.GET.get('project')
    nikimanager = NikiConverter()
    housetypes = nikimanager.getHouseTypes(project)
    result = "Woningtype,te huur, in optie, verhuurd\n"
    for housetype in housetypes:
        typename = housetype.get('name').replace(',', '&#44;')
        sale = housetype.get('houses').get('for-rent') if housetype.get('houses').get('for-rent') else 0
        option = housetype.get('houses').get('option') if housetype.get('houses').get('option') else 0
        sold = housetype.get('houses').get('rented') if housetype.get('houses').get('rented') else 0
        result += '{},{},{},{}\n'.format(typename, sale, option, sold)
    return HttpResponse(result)


def niki_interest_subscription_dates(request):
    """
    Return subscription dates and subscription count per date
    widget url: http://www.yourdomain.com/script?start_date={date_start}&end_date={date_end}
    """
    project_id = request.GET.get('project')
    start_str = request.GET.get('start_date')
    start = util.datestr_to_datetime(start_str)
    end_str = request.GET.get('end_date')
    end = util.datestr_to_datetime(end_str)

    interestmanager = InterestManager()
    project = InterestProject.objects.get(nikiProjectId=project_id)
    account = project.interestAccount
    ids = interestmanager.getIdsByProjectBetween(account, project_id, start, end)
    chart_data = ""
    if len(ids) > 0:
        subscriptions = interestmanager.getByIds(account, ids)
        dates = []  # list array of dates
        for subscription in subscriptions:
            posted = str(subscription.posted)[:-4]  # strip off time part
            dates.append(datetime.strptime(posted, "%Y%m%d"))
        counts = Counter(dates)
        # fill in the date gaps (create entries for non existing dates between start & end
        for single_date in daterange(start, end):
            if single_date not in counts:
                counts[single_date] = 0
        for key, value in counts.items():
            chart_data += "{},{}\n".format(datetime.strftime(key, "%Y%m%d"), value)

    result = "Date, Subscriptions\n"
    result += chart_data
    result += "Cumulative,0\n"
    result += "YAxisShow,1\n"
    return HttpResponse(result)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def nikiglobalstats(request):
    """
    Return a list of miscellanious project properties
    """
    projectcode = request.GET.get('project')
    nikimanager = NikiConverter()
    project = nikimanager.apiRequest(projectcode)
    result = "Projecteigenschap,Beschikbaar,Totaal\n"
    result += "Projectvoortgang,-,{}\n".format(project.get('progress'))
    result += "Aantal woningen,"
    return HttpResponse(result)
    """
        $result.= "Projectvoortgang,-,".$niki->getProject($this->project)->{'progress'}."\n";
        $result.= "Aantal woningen,".$availablecount.",".$niki->getTotalHouseCount($this->project)."\n";
        $priceRangeTotal = $niki->getProjectPropertyRange($this->project, 'price-range');
        $priceRangeAvailable = $niki->getProjectPropertyRange($this->project, 'price-range', true);
        $result.= "Prijsklasse vanaf,".$priceRangeAvailable['min'].",".$priceRangeTotal['min']."\n";
        $result.= "Prijsklasse tot,".$priceRangeAvailable['max'].",".$priceRangeTotal['max']."\n";
        $livingSurfaceRangeTotal = $niki->getProjectPropertyRange($project,'livingsurface-range');
        $livingSurfaceRangeAvailable = $niki->getProjectPropertyRange($project,'livingsurface-range',true);
        $result.= "Oppervlakte vanaf,".$livingSurfaceRangeAvailable['min'].",".$allHouseStats['livingSurfaceMin']."\n";
        $result.= "Oppervlakte tot,".$livingSurfaceRangeAvailable['max'].",".$allHouseStats['livingSurfaceMax']."\n";
        return $result;
    """


def mailchimp_list_activity(request):
    """
    Return aggregated info on list activity
    """
    params = request.GET
    if params.get('apikey') is not None:
        m = MailchimpManager(params.get('apikey'))
    else:
        return HttpResponse('BuzzartError: no Mailchimp Api key given (GET variable apikey)')
    api_response = m.api.lists.activity(params.get('lid'))
    result = 'Date,Subscribes,Unsubscribes,Mails sent,Opens,Clicks,Bounces\n'
    for item in api_response:
        date = item.get('day').replace('-', '')
        subs = item.get('subs')
        unsubs = item.get('unsubs')
        sent = item.get('emails_sent')
        opens = item.get('unique_opens')
        clicks = item.get('recipient_clicks')
        bounces = int(item.get('hard_bounce')) + int(item.get('soft_bounce'))
        result += '{},{},{},{},{},{}\n'.format(date, subs, unsubs, sent, opens, clicks, bounces)
    return HttpResponse(result)


def mailchimp_campaign_report(request):
    """
    Return report summary for campaign with id 'cid'
    """
    params = request.GET
    if params.get('apikey') is not None:
        m = MailchimpManager(params.get('apikey'))
    else:
        return HttpResponse('BuzzartError: no Mailchimp Api key given (GET variable apikey)')
    api_response = m.api.reports.summary(params.get('cid'))
    result = 'Emails sent,Unsubsribes,Bounces,Opens,Clicks\n'
    sent = api_response.get('emails_sent')
    unsubscribes = api_response.get('unsubscribes')
    bounces = int(api_response.get('hard_bounces')) + int(api_response.get('soft_bounces'))
    opens = api_response.get('opens')
    clicks = api_response.get('clicks')
    result += '{},{},{},{},{}\n'.format(sent, unsubscribes, bounces, opens, clicks)
    return HttpResponse(result)
