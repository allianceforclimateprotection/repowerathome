from django.conf.urls.defaults import *

urlpatterns = patterns("messaging.views",
    url(r"^(?P<token>.{30}).gif$", "open", name="message_open"),
)
