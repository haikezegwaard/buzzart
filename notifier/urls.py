from django.conf.urls import patterns, url
from django.contrib import admin
from views import DigestView, DirectTemplateView, MailView
import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'(?P<pk>\d+)/mailing', MailView.as_view(template_name='mailing.html', extra_context={ 'fallback': 1}),  name='mailing'),
    url(r'^(?P<pk>\d+)$', DigestView.as_view(template_name='digest.html', extra_context={ 'fallback': 1}),  name='digest'),
)