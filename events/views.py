from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from utils import forbidden

from invite.models import Invitation, make_token

from models import Event, Guest
from forms import EventForm, RsvpForm, GuestInviteForm, GuestAddForm, GuestListForm

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
    if not event.has_manager_privileges(request.user) and event.is_private:
        try:
            invite = Invitation.objects.get(token=token)
            if invite.content_object != event:
                return forbidden(request, "Invitation code is not valid for this event")
        except Invitation.DoesNotExist:
            return forbidden(request, "You need an invitation to view this event")
    rsvp_form = RsvpForm()
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
def guests(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = GuestListForm(event=event, data=(request.POST or None))
    if form.is_valid():
        response = form.save()
        return response if response else redirect("event-guests", event_id=event.id)
    return render_to_response("events/guests.html", locals(), context_instance=RequestContext(request))

@login_required
def guests_add(request, event_id, type):
    event = get_object_or_404(Event, id=event_id)
    guest = Guest(event=event)
    guest_add_form = GuestAddForm(instance=guest, data=(request.POST if type == "add" else None))
    if guest_add_form.is_valid():
        guest_add_form.save()
        return redirect("event-guests", event_id=event.id)
    invite = Invitation(user=request.user, content_object=event)
    guest_invite_form = GuestInviteForm(instance=invite, initial={"emails": request.GET.get("emails", "")},
        data=(request.POST if type == "invite" else None))
    if guest_invite_form.is_valid():
        guest_invite_form.save()
        return redirect("event-guests", event_id=event.id)
    return render_to_response("events/guests_add.html", locals(), context_instance=RequestContext(request))

@login_required
def commitments(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return redirect(event)
    
@require_POST
def rsvp(request):
    return redirect(events)
    
def print_sheet(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render_to_response("events/guests.html", locals(), context_instance=RequestContext(request))