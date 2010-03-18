from django.conf.urls.defaults import *

urlpatterns = patterns('invite.views',
    url(r'^welcome/(?P<token>[a-f0-9]{15})/$', 'invite_welcome', name='invite_welcome'),
    url(r'^rsvp/(?P<token>[a-f0-9]{15})/$', 'rsvp', name='rsvp'),
    url(r'^form/$', 'invite_form_handler', name='invite_form_handler'),
)