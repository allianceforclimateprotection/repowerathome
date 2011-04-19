from django.conf.urls.defaults import *

urlpatterns = patterns("flagged.views",
    # TODO: Make these underscores instead of hyphens
    url(r"^flag/$", "flag", name="flagged-flag"),
    url(r"^unflag/$", "unflag", name="flagged-unflag"),
)