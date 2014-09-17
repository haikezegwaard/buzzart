from django.shortcuts import render
from django.views.generic import TemplateView
from googleAnalytics.analyticsmanager import AnalyticsManager
from nikiInterest.interestmanager import InterestManager
from nikiInterest.models import InterestAccount
from datetime import date, datetime, timedelta
from niki.nikiconverter import NikiConverter
import xml.etree.ElementTree as ET
from monitor.models import Project
from facebook.fbmanager import FacebookManager
import logging
from mcapi.mailchimp_manager import MailchimpManager

class DirectTemplateView(TemplateView):
    """View to display template without model, adding context from parameters"""
    extra_context = None
    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.extra_context is not None:
            for key, value in self.extra_context.items():
                if callable(value):
                    context[key] = value()
                else:
                    context[key] = value

        return context

class DigestView(TemplateView):

    extra_context = None
    logger = logging.getLogger(__name__)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.extra_context is not None:
            for key, value in self.extra_context.items():
                if callable(value):
                    context[key] = value()
                else:
                    context[key] = value

        #dates for this mailing
        currentstart = datetime.today() - timedelta(days=15)
        currentend = datetime.today()

        previousstart = currentstart - timedelta(days = 15)
        previousend = currentstart


        #get testproject
        projectKey = self.kwargs['pk']
        project = Project.objects.get(id = projectKey)
        #project = Project.objects.get(name = context['projectname'])

        context['project'] = project

        #for testing purpose add content directly to context
        ga_manager = AnalyticsManager()
        ga_view = project.ga_view
        visits = ga_manager.get_weekly_visits(ga_view, currentstart.date().isoformat(), currentend.date().isoformat())
        context['traffic'] = visits['rows']

        context['traffic_target_sessions'] = 90
        context['traffic_target_pageviews'] = 300

        #Get Google Analytics conversions for this and previous period
        conversions = ga_manager.get_conversion_count_for_goal(ga_view, 1 ,currentstart.date().isoformat(), currentend.date().isoformat())
        context['conversions'] = conversions
        previous_conversions = ga_manager.get_conversion_count_for_goal(ga_view, 1, previousstart.date().isoformat(), previousend.date().isoformat())
        context['previous_conversions'] = previous_conversions

        #Get Google Analytics conversion rate for this and previous period
        self.logger.debug("analytics period: {} - {}".format(currentstart.date().isoformat(), currentend.date().isoformat()))
        conversion_rate = ga_manager.get_conversion_rate_for_goal(ga_view, 1, currentstart.date().isoformat(), currentend.date().isoformat())
        context['conversionrate'] = conversion_rate

        previous_conversion_rate = ga_manager.get_conversion_rate_for_goal(ga_view, 1, previousstart.date().isoformat(), previousend.date().isoformat())
        context['previousconversionrate'] = previous_conversion_rate

        #Get number of interested people from niki for this  and previous period
        interestManager = InterestManager()
        nip = interestManager.getNikiInterestProjectByProject(project)
        account = nip.interestAccount

        idlist = interestManager.getIdsByProjectBetween(account, nip.nikiProjectId, currentstart, currentend)
        context['interest'] = len(idlist)

        previousidlist = interestManager.getIdsByProjectBetween(account, nip.nikiProjectId, previousstart, previousend)
        context['previousinterest'] = len(previousidlist)

        context['interesttotal'] = len(interestManager.getIdsByProject(account, nip.nikiProjectId))

        #Get project Niki sales stats
        nikimanager = NikiConverter()
        context['availability'] = nikimanager.getAvailability(project.nikiProject)

        #Get the sex and age spread of likes on the fanpage
        fbmanager = FacebookManager()
        agesexspread = fbmanager.get_likes_sex_age_spread_sorted(project.fanpage_id)
        context['fbagesexspread'] = agesexspread


        #Get Mailchimp list growth statistics
        mcmanager = MailchimpManager(project.mailchimp_api_token)
        context['mailchimp'] = mcmanager.get_list_size_data(project.mailchimp_list_id)

        return context





