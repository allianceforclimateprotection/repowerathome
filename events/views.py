from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from models import Event
from forms import EventForm

@login_required
@csrf_protect
def create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        event = form.save()
        messages.success(request, "%s has been created." % event)
        return redirect(event)
    return render_to_response("events/create.html", locals(), context_instance=RequestContext(request))
        
def show(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render_to_response("events/show.html", locals(), context_instance=RequestContext(request))