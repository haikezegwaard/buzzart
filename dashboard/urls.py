from django.conf.urls import patterns, url
from django.contrib import admin
from django.views.generic import TemplateView
import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^plotdata/(?P<project_id>[0-9]*)', views.plottingDataSeries, name='plottingData'),
    url(r'^(?P<project_id>[0-9]*)$', views.index, name='home'),
    url(r'^(?P<project_id>[0-9]*)/origin$', views.origin, name='origin'),
    url(r'^(?P<project_id>[0-9]*)/updates', views.project_updates, name='updates'),
    url(r'^sitelist$', views.site_list, name='site_list'),
    url(r'^updates', views.corporate_updates, name='updates'),
    url(r'^FRX/radyus$', TemplateView.as_view(template_name='FRX/radyus/index.html')),
)
