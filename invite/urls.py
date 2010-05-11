from django.conf.urls.defaults import *

urlpatterns = patterns('invite.views',
    url(r'^welcome/(?P<token>[a-f0-9]{15})/$', 'invite_welcome', name='invite-welcome'),
    url(r'^rsvp/(?P<token>[a-f0-9]{15})/$', 'rsvp', name='invite-rsvp'),
    url(r'^invite/$', 'invite', name='invite-invite'),
)