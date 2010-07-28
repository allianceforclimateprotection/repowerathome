from django.conf.urls.defaults import *

urlpatterns = patterns("facebook_app.views",
    url(r"^login/$", "login", name="facebook_login"),
    url(r"^authorize/$", "authorize", name="facebook_authorize"),
    url(r"^unauthorize/$", "unauthorize", name="facebook_unauthorize"),
    url(r"^sharing/enable/$", "sharing", {"is_enabled": True}, name="facebook_enable_sharing"),
    url(r"^sharing/disable/$", "sharing", {"is_enabled": False}, name="facebook_disable_sharing"),
)