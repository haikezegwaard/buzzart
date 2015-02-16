from django.contrib.auth.models import User

from django.core.management.base import BaseCommand
from monitor.models import Summary
from django.conf import settings
from datetime import date
from datetime import timedelta

class Command(BaseCommand):

    args = 'date' # reset, update

    def handle(self, *args, **options):
        """
        For every summary in the summary table, create a new copy and set dates
        to new interval
        """

        for summary in Summary.objects.filter(mail_sent=True).all():
            print "duplicating summary id {}".format(summary.id)
            duplicate = Summary()
            duplicate.dateStart = date.today() - timedelta(days=14)
            duplicate.dateEnd = date.today()
            duplicate.introduction = summary.introduction
            duplicate.project = summary.project
            duplicate.traffic_advice = summary.traffic_advice
            duplicate.availability_advice = summary.availability_advice
            duplicate.facebook_advice = summary.facebook_advice
            duplicate.mailchimp_advice = summary.mailchimp_advice
            duplicate.conversion_advice = summary.conversion_advice
            duplicate.save()
