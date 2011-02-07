from django.shortcuts import render_to_response
from django.template import RequestContext

from brabeion import badges as badge_cache

from badges import all_badges_with_completion

def list(request):
    badges = all_badges_with_completion(request.user)
    return render_to_response('badges/list.html', locals(), context_instance=RequestContext(request))
