from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^conversionsTotal/(?P<project_id>[0-9]*)$', views.conversions_total, name='conversionsTotal'),
    url(r'^trafficThisWeek/(?P<project_id>[0-9]*)$', views.traffic_this_week, name='trafficThisWeek'),
    url(r'^traffic/(?P<project_id>[0-9]*)$', views.traffic, name='traffic'),
    url(r'^conversionsDaily/(?P<project_id>[0-9]*)$', views.conversions_daily, name='conversionsDaily'),
    url(r'^topPages/(?P<project_id>[0-9]*)$', views.top_pages, name='topPages'),
    url(r'^channelInfo/(?P<project_id>[0-9]*)$', views.channel_info, name='channelInfo'),
    url(r'^deviceCategory/(?P<project_id>[0-9]*)$', views.device_category, name='deviceCategory'),
    url(r'^accounts$', views.list_accounts, name='accounts'),
    url(r'^properties/(?P<account_id>.*)$', views.list_properties, name='properties'),
    url(r'^profiles/(?P<account_id>.*)/(?P<property_id>.*)$', views.list_profiles, name='profiles'),
    url(r'^findaccount/(?P<profile_id>.*)$', views.find_account, name='findaccount'),
    url(r'^goals/(?P<profile_id>.*)$', views.list_goals, name='goals')
    )