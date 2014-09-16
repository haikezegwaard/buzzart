from django.conf.urls import patterns, url
from django.contrib import admin
from views import DigestView, DirectTemplateView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'canvas$', DirectTemplateView.as_view(template_name='canvas.html', extra_context={ 'projectname': 'testproject'}),  name='canvas'),
    url(r'^$', DigestView.as_view(template_name='mailing.html', extra_context={ 'projectname': 'testproject'}),  name='digest')
)