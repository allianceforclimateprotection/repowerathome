import settings
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from rah.forms import AuthenticationForm
from basic.blog.feeds import BlogPostsFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

feeds = {
    'blog': BlogPostsFeed,
}

# OPTIMIZE: we can wrap the regex patterns in the url function to insure there are no reverse conflicts
urlpatterns = patterns('rah.views',
    url(r'^$', 'index', name='index'),
    # OPTIMIZE: we can remove our custom register view altogether and just specify our custom from as a parameter in the url pattern
    (r'^register/$', 'register'),
    (r'^account/$', 'account'),
    (r'^actions/$', 'action_show'),
    (r'^actions/(?P<action_slug>[a-z0-9-]+)/$', 'action_detail'),
    (r'^actiontasks/(?P<action_task_id>\d+)/$', 'action_task'),
    url(r'^user/(?P<user_id>\d+)/$', 'profile', name='profile'),
    url(r'^user/edit/(?P<user_id>\d+)/$', 'profile_edit', name='profile_edit'),
    (r'^validate/$', 'validate_field'),
    (r'^houseparty/$', 'house_party'),
    (r'^feedback/$', 'feedback'),
    (r'^search/$', 'search'),
    url(r'^comments/post/$', 'post_comment', name='post_comment'),
)

urlpatterns += patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^login/$', 'django.contrib.auth.views.login', { 'authentication_form': AuthenticationForm }),
    (r'^', include('django.contrib.auth.urls')),
    url(r'^admin/(.*)', admin.site.root, name='admin_root'),
    (r'^blog/', include('basic.blog.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^(?P<url>.*)/feed/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name='feed'),
    url(r'^twitter/', include('twitter_app.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^static/(?P<path>.*)$', 
        'serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': True }),)