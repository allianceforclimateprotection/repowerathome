import settings
from django.conf.urls.defaults import *
from rah.forms import AuthenticationForm, SetPasswordForm, PasswordChangeForm

from basic.blog.feeds import BlogPostsFeed
from groups.feeds import GroupActivityFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('rah.views',
    url(r'^$', 'index', name='index'),
    url(r'^register/$', 'register', name='register'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^password_change_done/$', 'password_change_done', name='password_change_done'),
    url(r'^password_reset_done/$', 'password_reset_done', name='password_reset_done'),
    url(r'^reset/done/$', 'password_reset_complete', name='password_reset_complete'),
    url(r'^user/(?P<user_id>\d+)/$', 'profile', name='profile'),
    url(r'^user/edit/(?P<user_id>\d+)/$', 'profile_edit', name='profile_edit'),
    (r'^validate/$', 'validate_field'),
    url(r'^houseparty/$', 'house_party', name='house_party'),
    url(r'^invitefriend/$', 'invite_friend', name='invite_friend'),
    url(r'^feedback/$', 'feedback', name='feedback'),
    (r'^search/$', 'search'),
    url(r'^terms/$', 'terms_of_use', name='terms_of_use'),
    url(r'^privacy/$', 'privacy_policy', name='privacy_policy'),
)

urlpatterns += patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', { 'authentication_form': AuthenticationForm }, name='login'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', { 'post_change_redirect': '/password_change_done/', 'password_change_form': PasswordChangeForm }, name='password_change'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', { 'post_reset_redirect': '/password_reset_done/' }, name='password_reset'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', { 'post_reset_redirect': '/reset/done/', 'set_password_form': SetPasswordForm }, name='password_reset_confirm'),
    (r'^', include('django.contrib.auth.urls')),
    url(r'^admin/(.*)', admin.site.root, name='admin_root'),
    (r'^blog/', include('basic.blog.urls')),
    url(r'^blog/feed/$', BlogPostsFeed(), name='blog_feed'),
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^twitter/', include('twitter_app.urls')),
    url(r'^rateable/', include('rateable.urls')),
    url(r'^groups/', include('groups.urls')),
    url(r'^invite/', include('invite.urls')),
    url(r'^flagged/flag/$', 'flagged.views.flag', name='flagged-flag'),
    url(r'^notifications/', include('notification.urls')),
    url(r'^actions/', include('actions.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^static/(?P<path>.*)$', 
        'serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': True }),)
        
urlpatterns += patterns('groups.views',
    url(r'^(?P<group_slug>[a-z0-9-]+)/$', 'group_detail', name='group_detail'),
    url(r'^(?P<group_slug>[a-z0-9-]+)/edit/$', 'group_edit', name='group_edit'),
    url(r'^(?P<group_slug>[a-z0-9-]+)/feed/$', GroupActivityFeed(), name='group_activity_feed'),
    url(r'^(?P<group_slug>[a-z0-9-]+)/discussions/$', 'group_disc_list', name='group_disc_list'),
    url(r'^(?P<group_slug>[a-z0-9-]+)/discussions/create/$', 'group_disc_create', name='group_disc_create'),
    url(r'^(?P<group_slug>[a-z0-9-]+)/discussions/(?P<disc_id>\d+)$', 'group_disc_detail', name='group_disc_detail'),
)