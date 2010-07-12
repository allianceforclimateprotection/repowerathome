from django.conf.urls.defaults import *

urlpatterns = patterns("messaging.views",
    url(r"^(?P<token>[a-z0-9]{30}).gif$", "open", name="message_open"),
    url(r"^(?P<token>[a-z0-9]{30})/$", "click", name="message_click"),
)
