from django.conf.urls import patterns, url

from niki import views

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^projects$', views.project_list, name='projectlist'),
                       url(r'^availability/(?P<project_id>[0-9]*)$', views.availability, name='availability'),
                       )
