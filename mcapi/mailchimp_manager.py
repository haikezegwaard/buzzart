from django.shortcuts import render
import mailchimp
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, loader
import logging
from datetime import datetime


class MailchimpManager:
    """
    Converter class to interface with Mailchimp API and
    retrieve project specific reporting data
    """

    def __init__(self, apikey):
        self.logger = logging.getLogger(__name__)
        try:
            self.api = mailchimp.Mailchimp(apikey)
        except:
            self.logger.error('could not initialize mc-api')
        

    def get_list_growth_data(self, listid):
        """
        Retrieve aggregated list growth stats for specific list
        """
        result = []
        try:
            result = self.api.lists.growth_history(listid)
        except mailchimp.Error:
            logging.error("Invalid API key")
        return result

    def get_list_size_data(self, listid):
        """
        Get a list of tuples containing (month, list size)
        """
        data = self.get_list_growth_data(listid)
        result = []
        for item in data:
            result.append((item.get('month'),int(item.get('existing'))))
        return sorted(result)

    def get_members(self, listid):
        return self.api.lists.members(listid)

    def get_campaigns(self, start, end, listid=None):
        """
        Return list of campaigns
        Start & end should be datetime objects
        if listid is specified, only campaigns sent to this list are returned
        """
        filters = {}
        if start is not None:
            filters['sendtime_start'] = self.mailchimp_date(start)
        if end is not None:
            filters['sendtime_end'] = self.mailchimp_date(end)
        if listid is not None:
            filters['list_id'] = listid
        result = self.api.campaigns.list(filters)
        self.logger.debug(result)
        return result

    def mailchimp_date(self, date):
        """
        Convert a python datetime object to the string format the Mailchimp
        api wants: 24h GMT format; "2013-12-30 20:30:00"
        """
        return datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
