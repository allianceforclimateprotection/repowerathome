from django.conf.urls.defaults import *

urlpatterns = patterns("export.views",
    url(r"^user/$", "user_export", name="user_export"),
)