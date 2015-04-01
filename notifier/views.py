from django.views.generic import TemplateView
from googleAnalytics.analyticsmanager import AnalyticsManager
from googleAnalytics.models import AnalyticsSettings
import util
from nikiInterest.interestmanager import InterestManager
from datetime import datetime, timedelta
import datetime
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
        summary = Summary.objects.get(id=summary_id)
        fill_context(context, summary)
        return context


class DigestTestView(TemplateView):
    """
    Create a mock summary object for last to weeks for given project and
    return digest context. For testing purposes
    """
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
        project_id = self.kwargs['pk']
        project = Project.objects.get(id=project_id)
        mock_summary = Summary()
        mock_summary.project = project
        mock_summary.dateStart = datetime.date.today() - timedelta(days=15)
        mock_summary.dateEnd = datetime.date.today() - timedelta(days=1)
        mock_summary.introduction = '''Nam quis nisi eu nulla accumsan congue nec nec enim. Pellentesque sit amet lorem ut augue lobortis iaculis. In elementum suscipit mauris elementum tincidunt. Curabitur pellentesque ullamcorper metus quis venenatis. Nunc urna ipsum, faucibus eu ex sit amet, pellentesque tincidunt est. Sed ullamcorper ipsum non iaculis consectetur. Cras sit amet leo vitae enim viverra auctor sit amet at mi. Proin non arcu eu ligula pharetra lacinia. Donec at metus eget tellus efficitur vulputate. Sed dignissim metus velit, et sollicitudin ex bibendum auctor. Integer ornare felis ante. Sed sit amet facilisis nulla. Nam dapibus maximus dignissim.'''
        mock_summary.facebook_advice = mock_summary.introduction
        mock_summary.availability_advice = mock_summary.introduction
        mock_summary.traffic_advice = mock_summary.introduction
        mock_summary.conversion_advice = mock_summary.introduction
        fill_context(context, mock_summary)

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
        summary = Summary.objects.get(id=summary_id)
        fill_context(context, summary)
        fetch_images(summary_id)
        # Check whether emailaddress is set, if so, send notification mail
        #if context['project'].email:
        plaintext_context = Context(autoescape=False)  # HTML escaping not appropriate in plaintext
        subject = render_to_string("mailsubject.txt", context, plaintext_context)
        text_body = render_to_string("sendmail.txt", context, plaintext_context)
        html_body = render_to_string("mailing.html", context)
        test = self.request.GET.get('test','no')
        if(test == 'no'):
            msg = EmailMultiAlternatives(subject=subject, from_email=settings.NOTIFIER_FROM_MAIL,
                                         to=[settings.ADMIN_MAIL,context['project'].email], body=text_body)
        else:
            msg = EmailMultiAlternatives(subject=subject, from_email=settings.NOTIFIER_FROM_MAIL,
                                         to=[settings.ADMIN_MAIL], body=text_body)
            summary.mail_sent = True
            summary.save()
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


def fill_context(context, summary):
    """Fetch all data and add to given dict"""

    logger = logging.getLogger(__name__)

    current_site = Site.objects.get_current()
    context['domain'] = current_site.domain


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
    if not ga_goal == '0':
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

    else:
        context['conversions'] = 0
        context['previous_conversions'] = 0
        context['total_conversions'] = 0
        context['conversionrate'] = 0
        context['previousconversionrate'] = 0
        context['total_conversion_rate'] = 0

    """ Get top pages """
    context['top_pages'] = ga_manager.get_top_pages(ga_view, currentstart, currentend)

    """ Get number of interested people from niki for this  and previous period """
    interestManager = InterestManager()
    nip = interestManager.getNikiInterestProjectByProject(project)
    idlist = []
    context['interest'] = 0
    context['previousinterest'] = 0
    context['interesttotal'] = 0
    if nip is not None:
        account = nip.interestAccount
        idlist = interestManager.getIdsByProjectBetween(account, nip.nikiProjectId, util.date_to_datetime(currentstart), util.date_to_datetime(currentend))
        logger.debug('fetched idlist from nikiinterest: {}'.format(idlist))
        context['interest'] = len(idlist)
        previousidlist = interestManager.getIdsByProjectBetween(account, nip.nikiProjectId, util.date_to_datetime(previousstart), util.date_to_datetime(previousend))
        context['previousinterest'] = len(previousidlist)
        interest_total = len(interestManager.getIdsByProject(account, nip.nikiProjectId))
        context['interesttotal'] = interest_total

    if(project.nikiProject != '0'):
        """ Get project Niki sales stats """
        nikimanager = NikiConverter()
        context['availability'] = nikimanager.getAvailability(project.nikiProject)
        context['nikisalerent'] = nikimanager.getProjectSaleRentType(project.nikiProject)
        if context['availability'] is not None:
            sold_count = context['availability'][2]
    if(project.fanpage_id != '0'):
        """ Get the sex and age spread of likes on the fanpage """
        fbmanager = FacebookManager()
        agesexspread = fbmanager.get_likes_sex_age_spread_sorted(project)
        if not agesexspread == []:
            context['fbagesexspread'] = agesexspread

    if(project.mailchimp_list_id != '0'):
        """ Get Mailchimp list growth statistics """
        mcmanager = MailchimpManager(project.mailchimp_api_token)
        context['mailchimp'] = mcmanager.get_list_growth_data(project.mailchimp_list_id)
    try:
        context['project_score'] = util.project_score(sold_count, interest_total, total_conversion_rate)
    except:
        context['project_score'] = 0
    return context
