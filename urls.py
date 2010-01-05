import settings
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from rah.forms import AuthenticationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# OPTIMIZE: we can wrap the regex patterns in the url function to insure there are no reverse conflicts
urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^login/$', 'django.contrib.auth.views.login', { 'authentication_form': AuthenticationForm }),
    (r'^', include('django.contrib.auth.urls')),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('rah.views',
    (r'^$', 'index'),
    # OPTIMIZE: we can remove our custom register view altogether and just specify our custom from as a parameter in the url pattern
    (r'^register/$', 'register'),
    (r'^account/$', 'account'),
    (r'^actions/$', 'action_show'),
    (r'^actions/(?P<action_slug>[a-z0-9-]+)/$', 'action_detail'),
    (r'^actiontasks/(?P<action_task_id>\d+)/$', 'action_task'),
    (r'^user/(?P<user_id>\d+)/$', 'profile'),
    (r'^user/edit/(?P<user_id>\d+)/$', 'profile_edit'),
    (r'^validate/$', 'validate_field'),
    (r'^houseparty/$', 'house_party'),
    (r'^feedback/$', 'feedback'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^static/(?P<path>.*)$', 
        'serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': True }),)