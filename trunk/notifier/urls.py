from django.conf.urls import patterns, url
from django.contrib import admin
from views import DigestView, DirectTemplateView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'canvas$', DirectTemplateView.as_view(template_name='canvas.html', extra_context={ 'projectname': 'testproject'}),  name='canvas'),
    url(r'^(?P<pk>\d+)$', DigestView.as_view(template_name='mailing.html', extra_context={ 'fallback': 1}),  name='digest')
)