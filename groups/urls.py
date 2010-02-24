from django.conf.urls.defaults import *

from feeds import GroupActivityFeed

urlpatterns = patterns('groups.views',
    url(r'^$', 'group_list', name='group_list'),
    url(r'^create/$', 'group_create', name='group_create'),
    url(r'^(?P<group_id>\d+)/leave/$', 'group_leave', name='group_leave'),
    url(r'^(?P<group_id>\d+)/join/$', 'group_join', name='group_join'),
    url(r'^(?P<group_id>\d+)/approve/(?P<user_id>\d+)/$', 'group_membership', {'action': 'approve'}, name='group_approve'),
    url(r'^(?P<group_id>\d+)/deny/(?P<user_id>\d+)/$', 'group_membership', {'action': 'deny'}, name='group_deny'),
    url(r'^(?P<state>[A-Z]{2})/(?P<county_slug>[a-z0-9-]+)/(?P<place_slug>[a-z0-9-]+)/$', 'geo_group', name='geo_group_place'),
    url(r'^(?P<state>[A-Z]{2})/(?P<county_slug>[a-z0-9-]+)/$', 'geo_group', name='geo_group_county'),
    url(r'^(?P<state>[A-Z]{2})/$', 'geo_group', name='geo_group_state'),
    url(r'^(?P<group_slug>[a-z0-9-]+)/$', 'group_detail', name='group_detail'),
    url(r'^(?P<group_slug>[a-z0-9-]+)/feed/$', GroupActivityFeed(), name='group_activity_feed'),
)