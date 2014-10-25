from django.conf.urls import patterns, url

from nikiInterest import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^subscriptionsTotal/(?P<project_id>[0-9]*)$', views.subscriptions_total, name='subscriptionsTotal'),
)