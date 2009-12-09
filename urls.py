from django.conf.urls.defaults import *
import settings

from django.core.urlresolvers import reverse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# OPTIMIZE: we can wrap the regex patterns in the url function to insure there are no reverse conflicts
urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),

    (r'^admin/', include(admin.site.urls)),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
)

urlpatterns += patterns('www.rah.views',
    (r'^$', 'index'),
    # OPTIMIZE: we can remove our custom register view altogether and just specify our custom from as a parameter in the url pattern
    (r'^register/$', 'register'),
    (r'^actions/$', 'action_browse'),
    (r'^actions/([a-z0-9-]+)/$', 'action_cat'),
    (r'^actions/([a-z0-9-]+)/([a-z0-9-]+)/$', 'action_detail'),
    (r'^(?P<username>\w+)/edit/$', 'profile_edit'),
    (r'^(?P<username>\w+)/$', 'profile'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^static/(?P<path>.*)$', 
        'serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': True }),)