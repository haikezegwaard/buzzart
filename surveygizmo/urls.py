'''
Created on Mar 27, 2015

@author: hz
'''
from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^survey/(?P<project_id>[0-9]*)$', views.get_survey, name='survey'),
                       url(r'^surveyreport/(?P<project_id>[0-9]*)$', views.get_survey_report, name='surveyreport'),
                       url(r'^surveystatistics/(?P<project_id>[0-9]*)$', views.get_survey_statistics, name='surveystatistics'),
                    )
