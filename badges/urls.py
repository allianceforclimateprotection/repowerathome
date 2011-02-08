from django.conf.urls.defaults import *

urlpatterns = patterns('badges.views',
    url(r'^$', 'list', name='badge_list'),
    url(r'^(?P<slug>[a-z0-9-]+)/$', 'detail', name='badge_detail'),
)
