from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from brabeion import badges as badge_cache
from brabeion.models import BadgeAward

import badges
from models import all_badges, get_badge

def list(request):
    nav_selected = "badges"
    badges = all_badges(request.user)
    return render_to_response('badges/list.html', locals(), context_instance=RequestContext(request))

def detail(request, slug):
    nav_selected = "badges"
    badge = get_badge(slug)
    if not badge:
        raise Http404('A badge %s does not exist' % slug)
    awardees = BadgeAward.objects.select_related().filter(slug=slug)
    return render_to_response('badges/detail.html', locals(), context_instance=RequestContext(request))
