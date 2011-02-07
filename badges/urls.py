from django.conf.urls.defaults import *

urlpatterns = patterns('badges.views',
    url(r'^$', 'list', name='badge_list'),
)
