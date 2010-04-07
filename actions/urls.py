from django.conf.urls.defaults import *

urlpatterns = patterns('actions.views',
    url(r'^$', 'action_show', name='action_show'),
    url(r'^tag/(?P<tag_slug>\w+)/$', 'action_show', name='action_tag'),
    url(r'^(?P<action_slug>[a-z0-9-]+)/$', 'action_detail', name='action_detail'),
    url(r'^(?P<action_slug>[a-z0-9-]+)/complete$', 'action_complete', name='action_complete'),
    url(r'^(?P<action_slug>[a-z0-9-]+)/undo$', 'action_undo', name='action_undo'),
    url(r'^(?P<action_slug>[a-z0-9-]+)/commit$', 'action_commit', name='action_commit'),
    url(r'^(?P<action_slug>[a-z0-9-]+)/cancel$', 'action_cancel', name='action_cancel'),
)