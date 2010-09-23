from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.http import urlquote

def attending(queryset):
    queryset.update(rsvp_status="A")
    
def not_attending(queryset):
    queryset.update(rsvp_status="N")
    
def invitation_email(queryset):
    emails = ", ".join([guest.contributor.email for guest in queryset])
    event_id = queryset.distinct().values_list("event__id", flat=True)[0]
    return HttpResponseRedirect(reverse("event-guests-add", args=[event_id]) + "?emails=" + urlquote(emails))
    
def announcement_email(queryset):
    event = queryset[0].event
    guest_ids = ",".join([str(guest.id) for guest in queryset])
    return HttpResponseRedirect(reverse("event-announcement", args=[event.id]) + "?guests=" + urlquote(guest_ids))
    
def reminder_email(queryset):
    event = queryset[0].event
    guest_ids = ",".join([str(guest.id) for guest in queryset])
    return HttpResponseRedirect(reverse("event-reminder", args=[event.id]) + "?guests=" + urlquote(guest_ids))
        
def remove(queryset):
    queryset.delete()
    
def make_host(queryset):
    queryset.update(is_host=True)
    
def unmake_host(queryset):
    # from django.db.models import Q, F
    # queryset.filter(Q(user__isnull=True)|~Q(event__creator=F("user"))).update(is_host=False)
    queryset.update(is_host=False)