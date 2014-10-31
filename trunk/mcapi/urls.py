from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mcapi_python_example.views.home', name='home'),
    # url(r'^mcapi_python_example/', include('mcapi_python_example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'chart_data_json', views.chart_data_json, name='chart_data_json'),
    url(r'campaign_stats', views.campaign_stats,name='campaign_stats'),
    url(r'list_campaigns', views.list_campaigns,name='list_campaigns'),
    #url(r'^lists/', include('lists.urls')),
    #url(r'^reports/', include('reports.urls'))

    )