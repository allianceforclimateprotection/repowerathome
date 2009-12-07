from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'www.rah.views.index'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^register/$', 'www.rah.views.register'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    (r'^actions/$', 'www.rah.views.action_browse'),
    (r'^actions/([a-z0-9-]+)/$', 'www.rah.views.action_cat'),
    (r'^actions/([a-z0-9-]+)/([a-z0-9-]+)/$', 'www.rah.views.action_detail'),
    (r'^inquiry/', 'www.rah.views.inquiry'),
    
    (r'^admin/', include(admin.site.urls)),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),

    (r'^(?P<username>.+)/$', 'www.rah.views.profile'),
)