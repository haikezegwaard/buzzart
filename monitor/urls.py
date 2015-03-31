from django.conf.urls import patterns, include, url
from django.conf import settings
from monitor import views
from django.contrib import admin
from djrill import DjrillAdminSite
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout


admin.site = DjrillAdminSite()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^project/(?P<pk>\d+)/$', views.ProjectDetail.as_view(), name='detail'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^niki/', include('niki.urls')),
    url(r'^twitter/', include('twitterAnalytics.urls')),
    url(r'^digest/', include('notifier.urls')),
    url(r'^nikiInterest/', include('nikiInterest.urls')),
    url(r'^facebook/', include('facebook.urls')),
    url(r'^cyfe/', include('cyfe.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^mailchimp/', include('mcapi.urls')),
    url(r'^sg/', include('surveygizmo.urls')),
    url(r'^googleAnalytics/', include('googleAnalytics.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^fbtokens',views.facebook_tokens, name='fbtokens'),
    url(r'^fbads', include('facebookAds.urls')),    
    url(r'^login/$', login, {'template_name':'login-form.html'}, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^$',views.index, name='index'),
    url(r'^setdates/$', views.set_reporting_date, name='set_dates'),
    url(r'^emailUpdate/(?P<update_id>\d+)/$', views.email_update, name='email_update'),
)# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
