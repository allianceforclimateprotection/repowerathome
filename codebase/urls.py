from django.conf.urls.defaults import *

urlpatterns = patterns("codebase.views",
    url(r"^feedback/$", "feedback", name="testing_feedback"),
)