from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'sexagespread/(?P<project_id>[0-9]*)$', views.fanpage_age_sex, name='fanpage_age_sex'),
    url(r'impressions/(?P<project_id>[0-9]*)$', views.fanpage_impressions, name='fanpage_impressions'),
    url(r'overview/(?P<project_id>[0-9]*)$', views.fanpage_overview, name='fanpage_overview'),
    url(r'impressions-by-city/(?P<project_id>[0-9]*)$', views.fanpage_impressions_by_city, name='fanpage_impressions_by_city'),

)

