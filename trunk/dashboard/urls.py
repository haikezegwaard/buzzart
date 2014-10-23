from django.conf.urls import patterns, url
from django.contrib import admin
import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^mockdata', views.mockDualSeries, name='mockData'),
    url(r'^$', views.index, name='home')
)
