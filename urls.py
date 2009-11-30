from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'www.splash.views.index'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^register/$', 'www.rah.views.register'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    (r'^home/$', 'www.rah.views.index'),
    (r'^actions/$', 'www.rah.views.actionBrowse'),
    (r'^actions/([a-z0-9-]+)/$', 'www.rah.views.actionCat'),
    (r'^actions/([a-z0-9-]+)/([a-z0-9-]+)/$', 'www.rah.views.actionDetail'),
    
    (r'^admin/', include(admin.site.urls)),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    
)