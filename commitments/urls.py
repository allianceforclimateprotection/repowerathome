from django.conf.urls.defaults import *

urlpatterns = patterns('commitments.views',
    url(r'^$', 'show', name='commitments_show'),
    url(r'^card/$', 'card_create', name='commitments_card_create'),
    url(r'^card/(?P<contributor>\d+)/$', 'card', name='commitments_card'),
)