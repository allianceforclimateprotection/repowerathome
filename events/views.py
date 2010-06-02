from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from utils import forbidden

from invite.models import Invitation, make_token

from models import Event, Guest
from forms import EventForm, GuestInviteForm, GuestAddForm, GuestListForm, RsvpForm, RsvpConfirmForm, RsvpAccountForm

@login_required
@csrf_protect
def create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        event = form.save(user=request.user)
        messages.success(request, "%s has been created." % event)
        return redirect(event)
    return render_to_response("events/create.html", locals(), context_instance=RequestContext(request))

def show(request, event_id, token=None):
    event = get_object_or_404(Event, id=event_id)
    if not event.is_guest(request) and event.is_private:
        if not token:
            return forbidden(request, "You need an invitation to view this event")
        if not event.is_token_valid(token):
            return forbidden(request, "Invitation code is not valid for this event")
    guest = event.current_guest(request, token)
    rsvp_form = RsvpForm(instance=guest, initial={"token": token})
    return render_to_response("events/show.html", locals(), context_instance=RequestContext(request))

@login_required
@csrf_protect
def edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = EventForm(instance=event, data=(request.POST or None))
    if form.is_valid():
        event = form.save(user=request.user)
        messages.success(request, "%s has been changed." % event)
        return redirect(event)
    return render_to_response("events/edit.html", locals(), context_instance=RequestContext(request))

@login_required
@csrf_protect
def guests(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = GuestListForm(event=event, data=(request.POST or None))
    if form.is_valid():
        response = form.save()
        return response if response else redirect("event-guests", event_id=event.id)
    return render_to_response("events/guests.html", locals(), context_instance=RequestContext(request))

@login_required
@csrf_protect
def guests_add(request, event_id, type):
    event = get_object_or_404(Event, id=event_id)
    guest = Guest(event=event)
    guest_add_form = GuestAddForm(instance=guest, data=(request.POST or None if type == "add" else None))
    if guest_add_form.is_valid():
        guest_add_form.save()
        return redirect("event-guests", event_id=event.id)
    invite = Invitation(user=request.user, content_object=event)
    guest_invite_form = GuestInviteForm(instance=invite, initial={"emails": request.GET.get("emails", "")},
        data=(request.POST or None if type == "invite" else None))
    if guest_invite_form.is_valid():
        guest_invite_form.save()
        return redirect("event-guests", event_id=event.id)
    return render_to_response("events/guests_add.html", locals(), context_instance=RequestContext(request))

@require_POST
@csrf_protect
def rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest = event.current_guest(request=request, token=request.POST.get("token", None))
    rsvp_form = RsvpForm(instance=guest, data=request.POST)
    if rsvp_form.is_valid():
        guest = rsvp_form.save(request)
        if guest.needs_more_info():
            return redirect("event-rsvp-confirm", event_id=event.id)
        else:
            return redirect(event)
    return render_to_response("events/show.html", locals(), context_instance=RequestContext(request))

@csrf_protect
def rsvp_confirm(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest = event.current_guest(request)
    form = RsvpConfirmForm(instance=guest, data=(request.POST or None))
    if form.is_valid():
        guest = form.save(request)
        return redirect("event-rsvp-account", event_id=event.id)
    return render_to_response("events/rsvp_confirm.html", locals(), context_instance=RequestContext(request))
    
@csrf_protect
def rsvp_account(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest = event.current_guest(request)
    form = RsvpAccountForm(instance=guest, data=(request.POST or None))
    if form.is_valid():
        guest = form.save(request)
        user = auth.authenticate(username=guest.email, password=form.cleaned_data["password1"])
        auth.login(request, user)
        return redirect(event)
    return render_to_response("events/rsvp_account.html", locals(), context_instance=RequestContext(request))
    
@login_required
def commitments(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return redirect(event)
        
def print_sheet(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render_to_response("events/guests.html", locals(), context_instance=RequestContext(request))