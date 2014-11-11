from django.conf.urls import patterns, url
from views import TwitterView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TwitterView.as_view(template_name='index.html', extra_context={ 'foo': 1}), name='index')
)