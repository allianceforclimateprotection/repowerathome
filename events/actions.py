from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import Q, F
from django.http import HttpResponseRedirect
from django.template import Context, loader
from django.utils.http import urlquote

def attending(queryset):
    queryset.update(rsvp_status="A")
    
def not_attending(queryset):
    queryset.update(rsvp_status="N")
    
def invitation_email(queryset):
    emails = ", ".join([guest.email for guest in queryset])
    event_id = queryset.distinct().values_list("event__id", flat=True)[0]
    return HttpResponseRedirect(reverse("event-guests-add", args=[event_id]) + "?emails=" + urlquote(emails))
    
def announcement_email(queryset):
    event = queryset[0].event
    _send_guest_emails(queryset, event, "%s Announcement" % event, "events/announcement_email.html")
    
def reminder_email(queryset):
    event = queryset[0].event
    _send_guest_emails(queryset, event, "%s Reminder" % event, "events/reminder_email.html")
    
def _send_guest_emails(queryset, event, subject, template):
    for guest in queryset:
        context = {"user": event.creator, "guest": guest, "domain": Site.objects.get_current().domain}
        msg = EmailMessage(subject, loader.render_to_string(template, context), None, [guest.email])
        msg.content_subtype = "html"
        msg.send()
        
def remove(queryset):
    queryset.delete()
    
def make_host(queryset):
    queryset.update(is_host=True)
    
def unmake_host(queryset):
    # not sure if this is right, but we only remove host privledges if the quest is not the creator
    queryset.filter(Q(user__isnull=True)|~Q(event__creator=F("user"))).update(is_host=False)