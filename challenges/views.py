from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST

from utils import forbidden

from models import Challenge
from forms import ChallengeForm, PetitionForm

def _edit(request, challenge):
    nav_selected = "challenges"
    form = ChallengeForm(instance=challenge, data=(request.POST or None))
    if form.is_valid():
        form.save()
        return redirect(challenge)
    type_label = challenge.id and 'Edit' or 'Create'
    return render_to_response('challenges/edit.html', locals(), context_instance=RequestContext(request))

def list(request):
    nav_selected = "challenges"
    challenges = Challenge.objects.all_challenges(request.user)
    return render_to_response('challenges/list.html', locals(), context_instance=RequestContext(request))

@login_required
def create(request):
    challenge = Challenge(creator=request.user)
    return _edit(request, challenge)

def detail(request, challenge_id):
    nav_selected = "challenges"
    challenge = get_object_or_404(Challenge.objects.select_related(), id=challenge_id)
    petition = PetitionForm(challenge=challenge, data=(request.POST or None))
    if petition.is_valid():
        petition.save()
        messages.success(request, 'Thanks for your support')
    return render_to_response('challenges/detail.html', locals(), context_instance=RequestContext(request))

@login_required
def edit(request, challenge_id=None):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    if request.user != challenge.creator:
        return forbidden(request, 'You do not have permissions to edit %s' % challenge)
    return _edit(request, challenge)
