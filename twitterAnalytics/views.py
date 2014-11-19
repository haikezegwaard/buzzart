from django.shortcuts import render
from django.http import HttpResponse
from TwitterAPI import TwitterAPI
import logging
from django.views.generic import TemplateView
from twittermanager import TwitterManager
# Create your views here.


class TwitterView(TemplateView):

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
        tm = TwitterManager()
        tm.get_follower_count('haikezegwaard')
        return context


