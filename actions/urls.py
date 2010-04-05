from django.conf.urls.defaults import *

urlpatterns = patterns('actions.views',
    url(r'^$', 'action_show', name='action_show'),
    url(r'^tag/(?P<tag_slug>\w+)/$', 'action_show', name='action_tag'),
    url(r'^(?P<action_slug>[a-z0-9-]+)/$', 'action_detail', name='action_detail'),
    url(r'^(?P<action_slug>[a-z0-9-]+)/commit$', 'action_commit', name='action_commit'),
)