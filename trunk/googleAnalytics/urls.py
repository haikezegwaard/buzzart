from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^conversionsTotal/(?P<project_id>[0-9]*)$', views.conversions_total, name='conversionsTotal'),
    url(r'^trafficThisWeek/(?P<project_id>[0-9]*)$', views.traffic_this_week, name='trafficThisWeek'),
    url(r'^conversionsDaily/(?P<project_id>[0-9]*)$', views.conversions_daily, name='conversionsDaily'),
    url(r'^channelInfo/(?P<project_id>[0-9]*)$', views.channel_info, name='channelInfo')
    )