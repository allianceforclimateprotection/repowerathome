from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from models import Invitation, Rsvp
from forms import InviteForm

@csrf_protect
@login_required
@require_POST
def invite(request, next=None):
    """Handles invite form submission"""
    invite_form = InviteForm(instance=Invitation(user=request.user), data=request.POST)
    if invite_form.is_valid():
        invites = invite_form.save()
        emails = ", ".join([invite.email for invite in invites])
        messages.success(request, 'Invitation sent to %s' % emails)
    else:
        messages.error(request, 'Form values where invalid, please try fill out the form again.')

    if request.is_ajax() and request.method == 'POST':
        message_html = loader.render_to_string('_messages.html', {}, RequestContext(request))
        return HttpResponse(message_html)

    next = request.POST.get("next", next)
    if next:
        return redirect(next)
    return redirect("index")

@login_required
def rsvp(request, token, next=None):
    invite = get_object_or_404(Invitation, token=token)
    if invite.user.pk != request.user.pk:
        rsvp, created = Rsvp.objects.get_or_create(invitee=request.user, invitation=invite)
        if created:
            messages.success(request, "Invitation from %s accepted" % invite.user.get_full_name())
        else:
            messages.info(request, "You already accepted this invitation from %s" % invite.user.get_full_name(),
                extra_tags="sticky")
    else:
        messages.info(request, "You cannot accept an invitation from yourself", extra_tags="sticky")

    next = request.GET.get("next", next)
    if next:
        return redirect(next)
    return redirect("index")

# def invite_welcome(request, token):
#     if request.user.is_authenticated():
#         return redirect("rsvp", token=token)
# 
#     try:
#         invite = Invitation.objects.select_related().get(token=token)
#     except Invitation.DoesNotExist:
#         messages.error(request, "Invitation not found.", extra_tags="sticky")
#         return redirect("index")
# 
#     return render_to_response("welcome.html", {
#         "invite": invite
#     }, context_instance=RequestContext(request))
