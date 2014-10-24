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
from monitor.models import InterestProject


# Create your views here.
def index(request, project_id):
    return render_to_response('home.html', {'project_id':project_id,
                                           'campaigns': get_campaigns(project_id),
                                           'traffic': get_traffic(project_id),
                                           'subscribers': get_subscriptions(project_id)},context_instance=RequestContext(request))


def get_campaigns(project_id):
    project = Project.objects.get(id=project_id)
    mc_man = MailchimpManager(project.mailchimp_api_token)
    start_date = datetime.datetime.today() - datetime.timedelta(days=31)
    end_date = datetime.datetime.today()
    start_str = datetime.datetime.strftime(start_date, '%Y-%m-%d %H:%M:%S')
    end_str = datetime.datetime.strftime(end_date, '%Y-%m-%d %H:%M:%S')
    json = mc_man.get_campaigns(start_str, end_str)
    result = []
    for item in json.get('data'):
        if(item.get('status') == 'sent'):
            dt = parser.parse(item.get('send_time'))
            result.append({'x':util.unix_time_millis(dt),'title': 'Mailing verstuurd', 'text':'Mailchimp campaign verstuurd:<br /><b>{}</b>'.format(item.get('title'))})
    return result


def get_traffic(project_id):
    project = Project.objects.get(id=project_id)
    ga_obj = AnalyticsSettings.objects.get(project=project)
    ga_man = AnalyticsManager()
    start_date = datetime.datetime.today() - datetime.timedelta(days=31)
    end_date = datetime.datetime.today()
    start_str = datetime.datetime.strftime(start_date,'%Y-%m-%d')
    end_str = datetime.datetime.strftime(end_date,'%Y-%m-%d')
    traffic = ga_man.get_daily_visits(ga_obj.ga_view, start_str, end_str)
    result = []
    for item in traffic.get('rows'):
        ms = util.unix_time_millis(parser.parse(item[0]))
        count = int(item[1])
        result.append([ms, count])
    return result


def get_subscriptions(project_id):

    project = Project.objects.get(id=project_id)
    interestManager = InterestManager()
    start_date = datetime.datetime.today() - datetime.timedelta(days=62)
    end_date = datetime.datetime.today()
    # array of SimpleXMLElements
    subscriptions = interestManager.getByProjectBetween(project, start_date, end_date)
    """
    # convert SimpleXMLElements, example:
    [<?xml version="1.0" encoding="UTF-8"?><subscription>
        <id>181398</id>
        <project externalId="003044" forSale="true">Appartementenvilla's Hofpark te Schagen</project>
        <projectowner id="450">Bot Bouw Initiatief</projectowner>
        <posted>201410210905</posted>
        <domain>hofpark-schagen.php-dev.fundament.nl</domain>
        <interests>
            <interest selected="true">
                <housetype externalId="GEN_D8EFF5F8-9806-43FF-A6F3-FC1682AA5D53">A2</housetype>
                <housemodel id="4">Appartement</housemodel>
                <pricemin>645000</pricemin>
                <pricemax>645000</pricemax>
            </interest>
            <interest selected="true">
                <housetype externalId="GEN_F6A95645-8B14-419D-9264-8D224D5E0BC0">C1</housetype>
                <housemodel id="4">Appartement</housemodel>
                <pricemin>373500</pricemin>
                <pricemax>376000</pricemax>
            </interest>
            <interest selected="true">
                <housetype externalId="GEN_715270A7-3957-4C20-807F-2786865AF579">C3</housetype>
                <housemodel id="4">Appartement</housemodel>
                <pricemin>565000</pricemin>
                <pricemax>565000</pricemax>
            </interest>
            <interest selected="true">
                <housetype externalId="GEN_3E5ECEEB-4870-4479-B892-D59887AC34AD">B1</housetype>
                <housemodel id="4">Appartement</housemodel>
                <pricemin>353500</pricemin>
                <pricemax>362500</pricemax>
            </interest>
            <interest selected="true">
                <housetype externalId="GEN_28F2D9F5-0FD2-4FB5-932F-EF3D0CA1D879">A1</housetype>
                <housemodel id="4">Appartement</housemodel>
                <pricemin>367000</pricemin>
                <pricemax>376000</pricemax>
            </interest>
        </interests>
        <subscribers>
            <subscriber type="subscriber">
                <id>425584</id>
                <initials>N</initials>
                <surname>Doorn</surname>
                <street>KPC de Bazelweg</street>
                <streetnumber>2</streetnumber>
                <streetnumberaddition/>
                <zipcode>1703DJ</zipcode>
                <city>HHW</city>
                <country>NL</country>
                <phonenumber>0652092098</phonenumber>
                <email>n.vandoorn@botbouwinitiatief.nl</email>
                <gender>M</gender>
            </subscriber>
            <subscriber type="partner">
                <id>425583</id>
                <streetnumberaddition/>
            </subscriber>
        </subscribers>
    </subscription>,...]
    """
    return subscriptions


def mockDualSeries(request):
    traffic = []
    subscriptions = []
    start_date = datetime.datetime.today() - datetime.timedelta(days=31)
    end_date = datetime.datetime.today()
    for single_date in util.daterange(start_date, end_date):
        traffic.append([util.unix_time_millis(single_date),random.randint(50, 150)])
        subscriptions.append([util.unix_time_millis(single_date),random.randint(0, 2)])

    data = [{"name": "data1", "data": get_traffic(1)},
            {"name": "data2", "data": subscriptions},
            {"name": "data3", "data": get_campaigns(1)}]
    return HttpResponse(json.dumps(data), content_type='application/json')