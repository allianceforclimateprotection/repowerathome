import csv
import datetime
import json
from pdf import render_to_pdf

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
from rah.forms import HousePartyForm
from rah.signals import logged_in
from invite.models import Invitation, make_token
from records.models import Record

from models import Event, Guest
from forms import EventForm, GuestInviteForm, GuestAddForm, GuestListForm, GuestEditForm, \
    RsvpForm, RsvpConfirmForm, RsvpAccountForm
from decorators import user_is_event_manager, user_is_guest, user_is_guest_or_has_token

def show(request):
    events = Event.objects.filter(is_private=False, when__gt=datetime.datetime.now()).order_by("when", "start")
    if request.user.is_authenticated():
        my_events = Event.objects.filter(guest__user=request.user)
    house_party_form = HousePartyForm(request.user)
    return render_to_response("events/show.html", locals(), context_instance=RequestContext(request))

@login_required
def create(request):
    form = EventForm(user=request.user, data=(request.POST or None))
    if form.is_valid():
        event = form.save()
        Record.objects.create_record(request.user, "event_create", event)
        messages.success(request, "%s has been created." % event)
        return redirect(event)
    return render_to_response("events/create.html", locals(), context_instance=RequestContext(request))

@user_is_guest_or_has_token
def detail(request, event_id, token=None):
    event = get_object_or_404(Event, id=event_id)
    guest = event.current_guest(request, token)
    if event.has_manager_privileges(request.user):
        template = "events/_detail.html" if request.is_ajax() else "events/detail.html"
    else:
        rsvp_form = RsvpForm(instance=guest, initial={"token": token, "rsvp_status": "A"})
        template = "events/rsvp.html"
    return render_to_response(template, locals(), context_instance=RequestContext(request))

@login_required
@user_is_event_manager
def edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = EventForm(user=request.user, instance=event, data=(request.POST or None))
    if form.is_valid():
        event = form.save()
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
        if response:
            return response
        if event.has_manager_privileges(request.user):
            return redirect("event-guests", event_id=event.id)
        else:
            return redirect(event)
    template = "events/_guests.html" if request.is_ajax() else "events/guests.html"
    return render_to_response(template, locals(), context_instance=RequestContext(request))

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
    template = "events/_guests_add.html" if request.is_ajax() else "events/guests_add.html"
    return render_to_response(template, locals(), context_instance=RequestContext(request))
    
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
    data = request.POST.copy()
    for field in guest._meta.fields:
        data[field.name] = field.value_from_object(guest)
    data[type] = data.get("value")
    form = GuestEditForm(instance=guest, data=data)
    if form.is_valid():
        form.save()
        messages.success(request, "%s has been updated" % guest)
    else:
        for field,errors in form.errors.items():
            for error in errors:
                messages.error(request, error)
    guest = Guest.objects.get(id=guest_id)
    message_html = render_to_string("_messages.html", {}, context_instance=RequestContext(request))
    guest_row = render_to_string("events/_guest_row.html", {"event": event, "guest": guest}, context_instance=RequestContext(request))
    return HttpResponse(json.dumps({"message_html": message_html, "guest_row": guest_row}), mimetype="text/json")

@require_POST
@user_is_guest_or_has_token
def rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest = event.current_guest(request=request, token=request.POST.get("token", None))
    rsvp_form = RsvpForm(instance=guest, data=request.POST)
    if rsvp_form.is_valid():
        guest = rsvp_form.store(request)
        if guest.needs_more_info():
            return redirect("event-rsvp-confirm", event_id=event.id)
        else:
            rsvp_form.save()
            return redirect(event)
    return render_to_response("events/show.html", locals(), context_instance=RequestContext(request))

@user_is_guest
def rsvp_confirm(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest = event.current_guest(request)
    form = RsvpConfirmForm(instance=guest, data=(request.POST or None))
    if form.is_valid():
        guest = form.save(request)
        if guest.user:
            return redirect(event)
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
        logged_in.send(sender=None, request=request, user=user, is_new_user=True)
        auth.login(request, user)
        return redirect(event)
    return render_to_response("events/rsvp_account.html", locals(), context_instance=RequestContext(request))
    
def rsvp_cancel(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete_guest_in_session(request)
    return redirect(event)
    
def rsvp_statuses(request):
    return HttpResponse(json.dumps(dict(Guest.RSVP_STATUSES)), mimetype="text/json")
    
@login_required
@user_is_event_manager
def commitments(request, event_id, guest_id=None):
    import survey_forms

    event = get_object_or_404(Event, id=event_id)
    if guest_id:
        guest = get_object_or_404(Guest, id=guest_id)
    else:
        guests = Guest.objects.filter(event=event)
        guest = guests[0] if len(guests) > 0 else None
    survey = event.survey()
    if survey:
        form = getattr(survey_forms, survey.form_name)(guest=guest, instance=survey, data=(request.POST or None))
        if form.is_valid():
            form.save()
            return redirect("event-commitments-guest", event_id=event.id, guest_id=event.next_guest(guest).id)
    template = "events/_commitments.html" if request.is_ajax() else "events/commitments.html"
    return render_to_response(template, locals(), context_instance=RequestContext(request))

@login_required
@user_is_event_manager
def print_sheet(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = event.attendees()
    attendee_count = len(attendees)

    # Fill every page with blank rows adding rows beyond the initial value of blank_rows if necessary
    blank_rows      = 10
    first_page_rows = 20
    page_rows       = 23
    if attendee_count + blank_rows <= first_page_rows:
        blank_rows = first_page_rows - attendee_count
    else:
        rows_after_first_page = attendee_count + blank_rows - first_page_rows
        if rows_after_first_page <= page_rows:
            blank_rows += page_rows - rows_after_first_page
        else: 
            blank_rows += page_rows - (rows_after_first_page % page_rows)
    
    blank_rows = range(blank_rows)
    return render_to_pdf("events/sign_in_sheet.html", "%s Sign In.pdf" % event, {
        "event": event, 
        "attendees": attendees, 
        "blank_rows": blank_rows
    })

@login_required
@user_is_event_manager
def spreadsheet(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    response = HttpResponse(mimetype="text/csv")
    response["Content-Disposition"] = "attachment; filename=%s Guest List.csv" % event
    
    questions = event.survey_questions()
    writer = csv.writer(response)
    writer.writerow(["Name", "Email", "Phone", "Zipcode", "Status"] + list(questions))
    
    for g in event.guests_with_commitments():
        answers = [getattr(g, question) for question in questions]
        writer.writerow([g.name, g.email, g.phone, g.zipcode, g.status()] + answers)
    
    return response