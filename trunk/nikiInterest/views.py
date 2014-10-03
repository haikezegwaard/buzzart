from django.shortcuts import render
from django.views import generic
from nikiInterest.models import InterestAccount
from nikiInterest.interestmanager import InterestManager
from datetime import date, datetime, timedelta
import xml.etree.ElementTree as ET

# Create your views here.
# Create your views here.

class IndexView(generic.TemplateView):

    #model = InterestAccount
    template_name = 'nikiInterest/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexView,self).get_context_data(**kwargs)
        start = datetime.today() - timedelta(days=14)
        # Add in a QuerySet of all the books
        interestManager = InterestManager()
        account = InterestAccount.objects.get(username='vanwijnen@fundament.nl')
        context['all'] = interestManager.getIdsByProject(account, 'GEN_630D1B86-31EE-494F-A718-48C8B6B4EA11')
        return context






