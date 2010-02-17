from django.conf.urls.defaults import *

urlpatterns = patterns("rateable.views",
    url(r"^rate/$", "rate", {"success_message": "Thank you for your rating."}, name="rateable-rate"),
)

urlpatterns += patterns('',
    url(r"^cr/(\d+)/(.+)/$", "django.views.defaults.shortcut", name="ratings-url-redirect"),
)