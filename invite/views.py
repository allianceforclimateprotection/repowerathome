from invite.models import Invitation, Rsvp
from invite.forms import InviteForm
from django.contrib import messages
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from utils import hash_val
import json

@csrf_protect
@login_required
def invite_form_handler(request):
    """Handles invite form submission"""
    if request.method == 'POST':
        invite_form = InviteForm(request.POST)
        if invite_form.is_valid():
            success_msg = 'Invitation sent to %s' % invite_form.cleaned_data['to_email']
            failure_msg = 'Whoops, something went wrong. That invitation was probably not sent. Try again?'
            if invite_form.save(request.user):
                messages.success(request, success_msg)
            else:
                messages.error(request, failure_msg)
            
            # If this isn't an ajax request, look for a return to
            redirect_to = request.POST.get('next', '')
            if redirect_to and '//' not in redirect_to:
                return HttpResponseRedirect(redirect_to)
    else:
        invite_form = InviteForm()
    return render_to_response("invite_form.html", {
        "invite_form": invite_form
    }, context_instance=RequestContext(request))

    
def invite_welcome(request, token):
    if request.user.is_authenticated():
        return redirect("rsvp", token=token)

    try:
        invite = Invitation.objects.select_related().get(token=token)
    except Invitation.DoesNotExist:
        messages.error(request, "Invitation not found.", extra_tags="sticky")
        return redirect("index")
        
    return render_to_response("welcome.html", {
        "invite": invite
    }, context_instance=RequestContext(request))


@login_required
def rsvp(request, token):
    invite = Invitation.objects.select_related().get(token=token)
    rsvp = Invitation.objects.rsvp(request.user, invite)
    if rsvp:
        messages.success(request, "Invitation from %s accepted" % invite.user.get_full_name())
    else:
        messages.info(request, "You already accepted this invitation from %s" % invite.user.get_full_name(), extra_tags="sticky")
    return redirect("index")