from django.conf.urls.defaults import *

urlpatterns = patterns('commitments.views',
    url(r'^$', 'commitment_show', name='commitment_show'),
    url(r'^card/$', 'commitment_card_create', name='commitment_card_create'),
    url(r'^card/(?P<contributor>\d+)/$', 'commitment_card', name='commitment_card'),
)