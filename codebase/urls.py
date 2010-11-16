from django.conf.urls.defaults import *

urlpatterns = patterns("codebase.views",
    url(r"^feedback/$", "feedback", name="testing_feedback"),
    url(r"^set_widget_opened/$", "set_wiget_state", {"opened": True}, name="testing_widget_opened"),
    url(r"^set_widget_closed/$", "set_wiget_state", {"opened": False}, name="testing_widget_closed"),
)