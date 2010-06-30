from django.conf.urls.defaults import *

urlpatterns = patterns("messaging.views",
    # TODO: Make these underscores instead of hyphens
    url(r"^(?P<token>.{30}).gif$", "open", name="message_open"),
)
