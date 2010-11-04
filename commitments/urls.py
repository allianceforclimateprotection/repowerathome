from django.conf.urls.defaults import *

urlpatterns = patterns('commitments.views',
    url(r'^$', 'show', name='commitments_show'),
    url(r'^card/$', 'card', name='commitments_card_create'),
    url(r'^card/(?P<contrib_id>\d+)/$', 'card', name='commitments_card'),
    url(r'^card/(?P<contrib_id>\d+)/(?P<form_name>\w+)/$', 'card', name='commitments_card_with_form'),
    url(r'^card/(?P<form_name>\w+)/$', 'card', name='new_commitment_card_with_form'),
    url(r'^take_pledge/$', 'take_pledge', name='take_pledge'),
)