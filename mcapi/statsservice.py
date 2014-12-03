from mailchimp_manager import MailchimpManager
from dateutil import parser
from dashboard import util
from operator import itemgetter
import logging

class StatsService():
    """
    Class for converting Mailchimp API data to graph/plotting format
    Target format is (mostly) list of tuples: [(timestamp,count)]
    """

    def __init__(self):
        """
        Construct me
        """
        self.logger = logging.getLogger(__name__)

    def get_campaigns_over_time(self, project, start, end):
        """
        Return a list of highchart flags tuples ({x, title, text}) representing
        the mailchimp campaigns available for token in project.
        """
        mc_man = MailchimpManager(project.mailchimp_api_token)
        json = mc_man.get_campaigns(start, end, project.mailchimp_list_id)
        result = []
        for item in json.get('data'):
            if(item.get('status') == 'sent'):
                dt = parser.parse(item.get('send_time'))
                result.append({'x':util.unix_time_millis(dt),
                               'title': 'M',
                               'text': u'Mailchimp campaign verstuurd: {}'.format(item.get('title'))})
        # sort the array of dicts by the value of x
        newlist = sorted(result, key=itemgetter('x'))
        return newlist

    def get_list_stats(self, project):
        """
        Return list stats for list specified in project
        (opt ins, existing, imports per month) formatted for use in Cyfe plot
        example js series:
        series: [{
            name: 'John',
            data: [5, 3, 4, 7, 2]
        }, {
            name: 'Jane',
            data: [2, 2, 3, 2, 1]
        }, {
            name: 'Joe',
            data: [3, 4, 4, 2, 5]
        }]
        """
        mc_man = MailchimpManager(project.mailchimp_api_token)
        list_growth = mc_man.get_list_growth_data(project.mailchimp_list_id)
        optins = {'name':'optins'}
        optins['data'] = []
        existing = {'name':'existing'}
        existing['data'] = []
        imports = {'name':'imports'}
        imports['data'] = []
        months = {'name' : 'months'}
        months['data'] = []
        for item in list_growth:
                optins['data'].append(item.get('optins'))
                existing['data'].append(item.get('existing'))
                imports['data'].append(item.get('imports'))
                months['data'].append(item.get('month'))
        result = []
        result.append(optins)
        result.append(existing)
        result.append(imports)
        result.append(months)
        return result
