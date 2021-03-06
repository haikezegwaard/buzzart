from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'monitor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^summary/(?P<pk>\d+)/$', views.ProjectSummaryMail.as_view(), name='summary'),
    url(r'niki/salecount/$', views.nikisalecount, name='salecount'),
    url(r'niki/rentcount/$', views.nikirentcount, name='rentcount'),
    url(r'niki/saletable/$', views.nikisaletable, name='saletable'),
    url(r'niki/renttable/$', views.nikirenttable, name='renttable'),
    url(r'niki/globalstats/$', views.nikiglobalstats, name='globalstats'),
    url(r'niki/subscriptions/$', views.niki_interest_subscription_dates, name='subscriptions'),
    url(r'niki/subscriptiontable/$', views.niki_interest_table, name='subscriptiontable'),
    url(r'mailchimp/listactivity/$', views.mailchimp_list_activity, name='mailchimp_list_activity'),
    url(r'mailchimp/campaignreport/$', views.mailchimp_campaign_report, name='mailchimp_campaign_report'),

)

