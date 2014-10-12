from TwitterAPI import TwitterAPI
import logging

class TwitterManager:

    def __init__(self):
        oauth_token = unicode('15916075-vCZIeZn3f4ksDz3Qg8RRgk4opE0rqhkOHkSR2GE4x')
        oauth_secret = 'Emoq1PJAn98K2mbjBT6hXkfxpmllMLuxwWFYZpBYOr4eD'
        consumer_secret = 'nyylZGieWcZYpylxocCGySDv5rcHwgTMXK9MOmeIbjqBbBKigW'
        consumer_key = 'pfhysTbUY4iTCVpdS3MwXHWPc'
        self.api = TwitterAPI(consumer_key, consumer_secret, oauth_token, oauth_secret)
        self.logger = logging.getLogger(__name__)

        #r = api.request('search/tweets', {'q':'pizza'})
        #for item in r.get_iterator():
        #    self.logger.debug(item)

    def get_follower_count(self, username):
        r = self.api.request('followers/list', {'screen_name':username})
        for item in r.get_iterator():
            self.logger.debug(item)
        return 'foo'