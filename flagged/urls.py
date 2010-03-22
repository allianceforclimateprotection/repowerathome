from django.conf.urls.defaults import *

urlpatterns = patterns("flagged.views",
    url(r"^flag/$", "flag", name="flagged-flag"),
    url(r"^unflag/$", "unflag", name="flagged-unflag"),
)