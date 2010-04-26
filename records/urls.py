from django.conf.urls.defaults import *

urlpatterns = patterns('records.views',
    url(r'^chart/(?P<user_id>\d+)/$', 'chart', name='records_chart'),
)