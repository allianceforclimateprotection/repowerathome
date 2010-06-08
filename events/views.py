import json

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models.fields import FieldDoesNotExist
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from utils import forbidden

from invite.models import Invitation, make_token

from models import Event, Guest, Survey, Challenge, Commitment
from forms import EventForm, GuestInviteForm, GuestAddForm, GuestListForm, \
    RsvpForm, RsvpConfirmForm, RsvpAccountForm, SurveyForm
from decorators import user_is_event_manager, user_is_guest, user_is_guest_or_has_token
from pdf import render_to_pdf

@login_required
def create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        event = form.save(user=request.user)
        messages.success(request, "%s has been created." % event)
        return redirect(event)
    return render_to_response("events/create.html", locals(), context_instance=RequestContext(request))

@user_is_guest_or_has_token
def show(request, event_id, token=None):
    event = get_object_or_404(Event, id=event_id)
    guest = event.current_guest(request, token)
    rsvp_form = RsvpForm(instance=guest, initial={"token": token})
    return render_to_response("events/show.html", locals(), context_instance=RequestContext(request))

@login_required
@user_is_event_manager
def edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = EventForm(instance=event, data=(request.POST or None))
    if form.is_valid():
        event = form.save(user=request.user)
        messages.success(request, "%s has been changed." % event)
        return redirect(event)
    return render_to_response("events/edit.html", locals(), context_instance=RequestContext(request))

@login_required
@user_is_event_manager
def guests(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = GuestListForm(event=event, data=(request.POST or None))
    if form.is_valid():
        response = form.save()
        return response if response else redirect("event-guests", event_id=event.id)
    return render_to_response("events/guests.html", locals(), context_instance=RequestContext(request))

@login_required
@user_is_event_manager
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
    
@login_required
@require_POST
@user_is_event_manager
def guests_edit(request, event_id, guest_id, type):
    event = get_object_or_404(Event, id=event_id)
    guest = get_object_or_404(Guest, id=guest_id)
    if guest.event != event:
        return forbidden(request, "Guest is not a member of this event")
    if not hasattr(guest, type):
        return forbidden(request, "Guest has no attribute %s" % type)
    value = request.POST.get("value", None)
    try:
        field = guest._meta.get_field(type)
        field.run_validators(value)
        var = setattr(guest, type, value)
        guest.save()
        messages.success(request, "%s has been updated" % guest)
    except FieldDoesNotExist:
        var = setattr(guest, type, value)
        guest.save()
        messages.success(request, "%s has been updated" % guest)
    except ValidationError as err:
        messages.error(request, err.messages[0])
    message_html = render_to_string("_messages.html", {}, context_instance=RequestContext(request))
    guest_row = render_to_string("events/_guest_row.html", {"event": event, "guest": guest}, context_instance=RequestContext(request))
    return HttpResponse(json.dumps({"message_html": message_html, "guest_row": guest_row}))

@require_POST
@user_is_guest_or_has_token
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

@user_is_guest
def rsvp_confirm(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest = event.current_guest(request)
    form = RsvpConfirmForm(instance=guest, data=(request.POST or None))
    if form.is_valid():
        guest = form.save(request)
        return redirect("event-rsvp-account", event_id=event.id)
    return render_to_response("events/rsvp_confirm.html", locals(), context_instance=RequestContext(request))

@user_is_guest
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
@user_is_event_manager
def commitments(request, event_id, guest_id=None):
    event = get_object_or_404(Event, id=event_id)
    if guest_id:
        guest = get_object_or_404(Guest, id=guest_id)
    else:
        guests = Guest.objects.filter(event=event)
        guest = guests[0] if len(guests) > 0 else None
    survey = Survey.objects.get(event_type=event.event_type, is_active=True)
    form = SurveyForm(guest=guest, instance=survey, data=(request.POST or None))
    if form.is_valid():
        form.save()
        redirect("event-commitments", event_id=event.id)
    return render_to_response("events/commitments.html", locals(), context_instance=RequestContext(request))
        
def print_sheet(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render_to_pdf("events/sign_in_sheet.html", { "event": event })