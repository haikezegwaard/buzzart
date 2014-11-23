from django.conf.urls import patterns, url
from django.contrib import admin
import views
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^/asyncjob/(?P<job>[0-9]*)$', views.asyncjob, name='asyncjob'),
                       url(r'^/jobstatus/(?P<job>[0-9]*)$', views.jobstatus, name='jobstatus'),

)