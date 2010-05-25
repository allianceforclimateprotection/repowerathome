from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from utils import forbidden

from invite.models import Invitation

from models import Event
from forms import EventForm, RsvpForm

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
    
def edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = EventForm(instance=event, data=(request.POST or None))
    if form.is_valid():
        event = form.save(user=request.user)
        messages.success(request, "%s has been changed." % event)
        return redirect(event)
    return render_to_response("events/edit.html", locals(), context_instance=RequestContext(request))
    
def guests(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return redirect(event)

def commitments(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return redirect(event)
    
@require_POST
def rsvp(request):
    return redirect(events)