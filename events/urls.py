from django.conf.urls.defaults import *

urlpatterns = patterns("events.views",
    url(r"^create/$", "create", name="event-create"),
    url(r"^show/(?P<event_id>\d+)/$", "show", name="event-show"),
    url(r"^edit/(?P<event_id>\d+)/$", "edit", name="event-edit"),
)