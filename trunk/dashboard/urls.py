from django.conf.urls import patterns, url
from django.contrib import admin
import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^plotdata/(?P<project_id>[0-9]*)', views.plottingDataSeries, name='plottingData'),
    url(r'^(?P<project_id>[0-9]*)$', views.index, name='home')
)
