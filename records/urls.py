from django.conf.urls.defaults import *

urlpatterns = patterns('records.views',
    url(r'^chart/(?P<user_id>\d+)/$', 'chart', name='records_chart'),
    url(r'^ask_to_share/$', 'ask_to_share', name='records_ask_to_share'),
    url(r'^dont_ask_again/$', 'dont_ask_again', name='records_dont_ask_again'),
)