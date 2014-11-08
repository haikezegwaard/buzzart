from django.conf.urls import patterns, url

from niki import views

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^projects$', views.project_list, name='projectlist')
                       )
