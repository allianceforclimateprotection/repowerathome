from django.conf.urls.defaults import *

urlpatterns = patterns("events.views",
    url(r"^create/$", "create", name="event-create"),
    url(r"^(?P<event_id>\d+)/$", "show", name="event-show"),
    url(r"^(?P<event_id>\d+)/invite/(?P<token>[a-f0-9]{15})/$", "show", name="event-show-invite"),
    url(r"^(?P<event_id>\d+)/edit/$", "edit", name="event-edit"),
    url(r"^(?P<event_id>\d+)/guests/$", "guests", name="event-guests"),
    url(r"^(?P<event_id>\d+)/guests/add/", "guests_add", name="event-guests-add"),
    url(r"^(?P<event_id>\d+)/guests/invite/", "guests_invite", name="event-guests-invite"),
    url(r"^(?P<event_id>\d+)/commitments/$", "commitments", name="event-commitments"),
    url(r"^/rsvp/$", "rsvp", name="event-rsvp"),
    url(r"^(?P<event_id>\d+)/print/$", "print_sheet", name="event-print"),
)