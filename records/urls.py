from django.conf.urls.defaults import *

urlpatterns = patterns('records.views',
    url(r'^chart/(?P<user_id>\d+)/$', 'chart', name='records_chart'),
    url(r'^ask_to_share/$', 'ask_to_share', name='records_ask_to_share'),
)