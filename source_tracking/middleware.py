import re

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from rah.signals import logged_in

from models import UserSource

DOMAIN = re.compile("https?://%s" % Site.objects.get_current().domain)
STK = "source_tracking_key"

class SourceTrackingMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            return None
        referrer = request.META.get("HTTP_REFERER", None)
        if referrer and not re.search(DOMAIN, referrer):
            codes = {"source": request.GET.get("source", ""), 
                "subsource": request.GET.get("subsource", ""),
                "referrer": referrer}
            request.session[STK] = codes
            
def add_source_tracking(sender, request, user, is_new_user, **kwargs):
    if is_new_user:
        codes = request.session.pop(STK, {"source": "direct"})
        UserSource.objects.create(user=user, source=codes.get("source", ""),
            subsource=codes.get("subsource", ""), referrer=codes.get("referrer", ""))
logged_in.connect(add_source_tracking)