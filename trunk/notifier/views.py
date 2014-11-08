from django.views.generic import TemplateView
from googleAnalytics.analyticsmanager import AnalyticsManager
from googleAnalytics.models import AnalyticsSettings
import util
from nikiInterest.interestmanager import InterestManager
from datetime import datetime, timedelta
from niki.nikiconverter import NikiConverter
from monitor.models import Project
from facebook.fbmanager import FacebookManager
import logging
from mcapi.mailchimp_manager import MailchimpManager
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template import RequestContext
from monitor.models import Summary
import timeit
from django.contrib.sites.models import Site
from django.conf import settings

logger = logging.getLogger(__name__)


class DirectTemplateView(TemplateView):
    """
    View to display template without model,
    adding context from parameters
    """
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

        # get testproject
        summary_id = self.kwargs['pk']
        fill_context(context, summary_id)
        return context


class MailView(TemplateView):

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

        summary_id = self.kwargs['pk']
        fill_context(context, summary_id)
        fetch_images(summary_id)
        # Check whether emailaddress is set, if so, send notification mail
        #if context['project'].email:
        plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext
        subject = render_to_string("mailsubject.txt", context, plaintext_context)
        text_body = render_to_string("sendmail.txt", context, plaintext_context)
        html_body = render_to_string("mailing.html", context)
        msg = EmailMultiAlternatives(subject=subject, from_email=settings.NOTIFIER_FROM_MAIL,
                                         to=[settings.ADMIN_MAIL,context['project'].email], body=text_body)
        msg.attach_alternative(html_body, "text/html")
        msg.send()

        return context


def fetch_images(summary_id):
    current_site = Site.objects.get_current()
    domain = current_site.domain
    logger.debug('domain of current site: {}'.format(domain))
    url = 'http://{}/digest/{}'.format(domain, summary_id)
    util.store_remote_images(url, summary_id)
    return "fetched images"


def fill_context(context, summary_id):
    """Fetch all data and add to given dict"""

    logger = logging.getLogger(__name__)

    current_site = Site.objects.get_current()
    context['domain'] = current_site.domain

    summary = Summary.objects.get(id=summary_id)
    context['summary'] = summary
    """ Fetch project from summary """
    project = summary.project
    context['project'] = project

    """ dates for this mailing """
    currentstart = summary.dateStart
    currentend = summary.dateEnd

    previousstart = summary.dateStart - timedelta(days=15)
    previousend = summary.dateStart

    """ Fetch Analytics settings for this project """
    ga_settings = AnalyticsSettings.objects.get(project=project)
    logger.debug("fetched analytics settings: {}".format(ga_settings))
    ga_view = ga_settings.ga_view
    ga_goal = ga_settings.goal_to_track

    """ for testing purpose add content directly to context """
    ga_manager = AnalyticsManager()

    visits = ga_manager.get_weekly_visits(ga_view, currentstart.isoformat(), currentend.isoformat())
    context['traffic'] = visits['rows']

    context['traffic_target_sessions'] = ga_settings.sessions_target
    context['traffic_target_pageviews'] = ga_settings.pageviews_target

    """ Get Google Analytics conversions for this and previous period """
    conversions = ga_manager.get_conversion_count_for_goal(ga_view, ga_goal , currentstart.isoformat(), currentend.isoformat())
    context['conversions'] = conversions
    previous_conversions = ga_manager.get_conversion_count_for_goal(ga_view, ga_goal, previousstart.isoformat(), previousend.isoformat())
    context['previous_conversions'] = previous_conversions
    total_conversions = ga_manager.get_conversion_count_for_goal(ga_view, ga_goal, ga_manager.GA_NULL_DATE, currentend.isoformat())
    context['total_conversions'] = total_conversions

    """ Get Google Analytics conversion rate for this and previous period """
    logger.debug("analytics period: {} - {}".format(currentstart.isoformat(), currentend.isoformat()))
    conversion_rate = ga_manager.get_conversion_rate_for_goal(ga_view, ga_goal, currentstart.isoformat(), currentend.isoformat())
    context['conversionrate'] = conversion_rate

    previous_conversion_rate = ga_manager.get_conversion_rate_for_goal(ga_view, ga_goal, previousstart.isoformat(), previousend.isoformat())
    context['previousconversionrate'] = previous_conversion_rate

    total_conversion_rate = ga_manager.get_conversion_rate_for_goal(ga_view, ga_goal, ga_manager.GA_NULL_DATE, currentend.isoformat())
    context['total_conversion_rate'] = total_conversion_rate

    """ Get number of interested people from niki for this  and previous period """
    interestManager = InterestManager()
    nip = interestManager.getNikiInterestProjectByProject(project)
    account = nip.interestAccount
    idlist = interestManager.getIdsByProjectBetween(account, nip.nikiProjectId, util.date_to_datetime(currentstart), util.date_to_datetime(currentend))
    logger.debug('fetched idlist from nikiinterest: {}'.format(idlist))
    context['interest'] = len(idlist)

    previousidlist = interestManager.getIdsByProjectBetween(account, nip.nikiProjectId, util.date_to_datetime(previousstart), util.date_to_datetime(previousend))
    context['previousinterest'] = len(previousidlist)

    interest_total = len(interestManager.getIdsByProject(account, nip.nikiProjectId))
    context['interesttotal'] = interest_total

    """ Get project Niki sales stats """
    nikimanager = NikiConverter()
    context['availability'] = nikimanager.getAvailability(project.nikiProject)

    if(project.fanpage_id != '0'):
        """ Get the sex and age spread of likes on the fanpage """
        fbmanager = FacebookManager()
        agesexspread = fbmanager.get_likes_sex_age_spread_sorted(project.fanpage_id)
        context['fbagesexspread'] = agesexspread

    if(project.mailchimp_list_id != '0'):
        """ Get Mailchimp list growth statistics """
        mcmanager = MailchimpManager(project.mailchimp_api_token)
        context['mailchimp'] = mcmanager.get_list_growth_data(project.mailchimp_list_id)

    sold_count = context['availability'][2]
    context['project_score'] = util.project_score(sold_count, interest_total, total_conversion_rate)
    return context





