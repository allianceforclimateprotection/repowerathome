from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

from models import Commitment

@login_required
def show(request):
    commitments = Commitment.objects.distinct().select_related('action__id', 'action__name', 
        'contributor__first_name', 'contributor__last_name', 'contributor__email', 
        'contributor__user__first_name', 'contributor__user__last_name','contirbutor__user__email').filter(
        contributor__contributorsurvey__entered_by=request.user, action__isnull=False).order_by(
        'contributor__first_name', 'contributor__last_name')
    actions = {}
    for c in commitments:
        if c.action in actions:
            actions[c.action].append(c)
        else:
            actions[c.action] = [c]
    total_commitments = 0
    total_completes = 0
    for a, c in actions.items():
        commitments = len([x for x in c if x.answer == 'C'])
        total_commitments += commitments
        completes = len([x for x in c if x.answer == 'D'])
        total_completes += completes
        actions[a] = (c, commitments, completes)
    return render_to_response('commitments/show.html', locals(), context_instance=RequestContext(request))
    
def card(request, contributor=None):
    return render_to_response('commitments/card.html', {}, context_instance=RequestContext(request))