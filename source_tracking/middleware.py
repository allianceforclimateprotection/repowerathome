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
        codes = request.session.get(STK, {})
        source = request.GET.get("source", None)
        subsource = request.GET.get("subsource", None)
        if source or subsource:
            codes["source"] = source or ""
            codes["subsource"] = subsource or ""
        referrer = request.META.get("HTTP_REFERER", None)
        if referrer and not re.search(DOMAIN, referrer):
            codes["referrer"] = referrer
        if codes.items():
            request.session[STK] = codes
            
def add_source_tracking(sender, request, user, is_new_user, **kwargs):
    if is_new_user:
        codes = request.session.pop(STK, {"source": "direct"})
        UserSource.objects.create(user=user, source=codes.get("source", ""),
            subsource=codes.get("subsource", ""), referrer=codes.get("referrer", ""))
logged_in.connect(add_source_tracking)