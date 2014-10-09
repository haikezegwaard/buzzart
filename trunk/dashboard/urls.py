from django.conf.urls import patterns, url
from django.contrib import admin
from django.conf import settings
import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',views.index, name='index'),
    url(r'^map/$',views.javamap,name='map')
)