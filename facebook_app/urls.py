from django.conf.urls.defaults import *

urlpatterns = patterns("facebook_app.views",
    url(r"^login/$", "login", name="facebook_login"),
)