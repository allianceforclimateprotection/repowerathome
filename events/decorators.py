from functools import wraps

from django.shortcuts import get_object_or_404
from django.utils.decorators import available_attrs

from utils import forbidden

from models import Event

def user_is_event_manager(view_func):
    def _wrapped_view(request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, id=event_id)
        if event.has_manager_privileges(request.user):
            return view_func(request, event_id, *args, **kwargs)
        return forbidden(request, "You must be an event manager")
    return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    
def user_is_guest(view_func):
    def _wrapped_view(request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, id=event_id)
        if not event.is_guest(request):
            return forbidden(request, "You are not a registered guest")
        return view_func(request, event_id, *args, **kwargs)
    return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    
def user_is_guest_or_has_token(view_func):
    def _wrapped_view(request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, id=event_id)
        if not event.is_guest(request) and event.is_private:
            token = kwargs.get("token", request.POST.get("token", None))
            if not token:
                return forbidden(request, "You need an invitation for this event")
            if not event.is_token_valid(token):
                return forbidden(request, "Invitation code is not valid for this event")
        return view_func(request, event_id, *args, **kwargs)
    return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
