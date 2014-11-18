from facebookads.api import FacebookAdsApi
from facebookads import objects
from django.conf import settings
from facebookads.objects import AdCampaign

class FacebookAdsManager:


    def campaign_stats(self, account):

        result = ">>> Campaign Stats"
        for campaign in account.get_ad_campaigns(fields=[AdCampaign.Field.name]):
            for stat in campaign.get_stats(fields=[
                'impressions',
                'clicks',
                'spent',
                'unique_clicks',
                'actions',
            ]):
                result = "{}{}<br />\n".format(result, campaign[campaign.Field.name])
                for statfield in stat:
                    result += "\t%s:\t\t%s<br/>" % (statfield, stat[statfield])