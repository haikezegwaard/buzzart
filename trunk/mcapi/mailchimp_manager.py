from django.shortcuts import render
import mailchimp
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, loader
import logging

class MailchimpManager:
    """
    Converter class to interface with Mailchimp API and
    retrieve project specific reporting data
    """


    def __init__(self, apikey):
        self.api = mailchimp.Mailchimp(apikey)

    def get_list_growth_data(self, listid):
        """
        Retrieve aggregated list growth stats for specific list
        """
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
