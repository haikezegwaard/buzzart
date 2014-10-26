import mailchimp_manager
from dateutil import parser
from dashboard import util
from operator import itemgetter

class StatsService():
    """
    Class for converting Mailchimp API data to graph/plotting format
    Target format is (mostly) list of tuples: [(timestamp,count)]
    """

    def __init__(self):
        """
        Construct me
        """

    def get_campaigns_over_time(self, project, start, end):
        """
        Return a list of highchart flags tuples ({x, title, text}) representing
        the mailchimp campaigns available for token in project.
        """
        mc_man = mailchimp_manager.MailchimpManager(project.mailchimp_api_token)
        json = mc_man.get_campaigns(start, end)
        result = []
        for item in json.get('data'):
            if(item.get('status') == 'sent'):
                dt = parser.parse(item.get('send_time'))
                result.append({'x':util.unix_time_millis(dt),'title': 'Mailing verstuurd', 'text':'Mailchimp campaign verstuurd:<br /><b>{}</b>'.format(item.get('title'))})
        # sort the array of dicts by the value of x
        newlist = sorted(result, key=itemgetter('x'))
        return newlist
