from django.conf.urls.defaults import *

urlpatterns = patterns("events.views",
    url(r"^show/(?P<event_id>\d+)/$", "show", name="event-show"),
    url(r"^create/$", "create", name="event-create"),
)