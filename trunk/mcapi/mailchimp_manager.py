import mailchimp
import logging


class MailchimpManager:
    """
    Converter class to interface with Mailchimp API and
    retrieve project specific reporting data
    """

    def __init__(self, apikey):
        self.api = mailchimp.Mailchimp(apikey)
        self.logger = logging.getLogger(__name__)

    def get_list_growth_data(self, listid):
        """
        Retrieve aggregated list growth stats for specific list
        """
        try:
            result = self.api.lists.growth_history(listid)
            self.logger.debug('Got from mailchimp api: {}'.format(result))
        except mailchimp.Error:
            self.logger.error("Invalid API key")
        return result

    def get_list_size_data(self, listid):
        """
        Get a list of tuples containing (month, list size)
        """
        data = self.get_list_growth_data(listid)
        result = []
        for item in data:
            result.append((item.get('month'), int(item.get('existing'))))
            self.logger.debug('Got from mailchimp api: {}'.format(result))
        return sorted(result)

    def get_list_members(self, listid):
        self.api.lists.members(listid)
