import re

from django.http import HttpResponseRedirect
from django.utils.http import urlquote

from models import MessageLink

class LinkTrackingMiddleware(object):
    TOKEN_PATTERN = re.compile(r"^(.+/)([^/]{30})/$")
    
    def process_request(self, request):
        match = LinkTrackingMiddleware.TOKEN_PATTERN.search(request.path)
        if not match:
            return
            
        token = match.group(2)
        try:
            ml = MessageLink.objects.get(token=token)
            ml.clicks += 1
            ml.save()
        except MessageLink.DoesNotExist:
            pass
        newurl = "%s://%s%s" % (
            request.is_secure() and 'https' or 'http',
            request.get_host(), urlquote(match.group(1)))
        return HttpResponseRedirect(newurl)