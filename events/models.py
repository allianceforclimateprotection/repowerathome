import datetime

from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.db import models
from django.template import Context, loader
from django.utils.dateformat import DateFormat

from invite.models import Invitation

class EventType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    teaser = models.CharField(max_length=150)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class Event(models.Model):
    creator = models.ForeignKey("auth.User")
    event_type = models.ForeignKey(EventType, default="")
    where = models.CharField(max_length=100)
    location = models.ForeignKey("geo.Location", null=True)
    when = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    details = models.TextField(help_text="For example, where should people park,\
        what's the nearest subway, do people need to be buzzed in, etc.")
    is_private = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u"%s in %s" % (self.event_type, self.location)
        
    @models.permalink
    def get_absolute_url(self):
        return ("event-show", [str(self.id)])
        
    def place(self):
        return "%s %s" % (self.where, self.location)
        
    def has_manager_privileges(self, user):
        if not user.is_authenticated():
            return False
        return user == self.creator or \
            Guest.objects.filter(event=self, user=user, is_host=True).exists()
            
    def is_guest(self, request):
        user = request.user
        if not user.is_authenticated():
            return self._guest_key() in request.session
        return user == self.creator or \
            Guest.objects.filter(event=self, user=user).exists()
        
    def confirmed_guests(self):
        return Guest.objects.filter(event=self, rsvp_status="A").count()
        
    def outstanding_invitations(self):
        return Guest.objects.filter(event=self, invited__isnull=False, rsvp_status="").count()
        
    def is_token_valid(self, token):
        try:
            invite = Invitation.objects.get(token=token)
            return invite.content_object == self
        except Invitation.DoesNotExist:
            return False
            
    def _guest_key(self):
        return "event_%d_guest" % self.id
            
    def current_guest(self, request, token=None):
        if request.user.is_authenticated():
            try:
             return Guest.objects.get(event=self, user=request.user)
            except Guest.DoesNotExist:
                pass
        if self._guest_key() in request.session:
            return request.session[self._guest_key()]
        if token:
            try:
                invite = Invitation.objects.get(token=token)
                guest = Guest.objects.get(event=self, email=invite.email)
                if not guest.rsvp_status:
                    return guest
            except Invitation.DoesNotExist:
                pass
            except Guest.DoesNotExist:
                pass
        return Guest(event=self)
        
    def save_guest_in_session(self, request, guest):
        request.session[self._guest_key()] = guest
        
class Guest(models.Model):
    RSVP_STATUSES = (
        ("A", "Attending",),
        ("M", "Maybe Attending",),
        ("N", "Not Attending",),
    )
    event = models.ForeignKey(Event)
    first_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(blank=True, max_length=50)
    email = models.EmailField(blank=True)
    phone = models.CharField(blank=True, max_length=12)
    invited = models.DateField(null=True, blank=True)
    added = models.DateField(null=True, blank=True)
    rsvp_status = models.CharField(blank=True, max_length=1, choices=RSVP_STATUSES)
    notify_on_rsvp = models.BooleanField(default=False)
    is_host = models.BooleanField(default=False)
    user = models.ForeignKey("auth.User", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def status(self):
        if self.rsvp_status:
            return self.get_rsvp_status_display()
        if self.invited:
            return "Invited %s" % DateFormat(self.invited).format("M j")
        if self.added:
            return "Added %s" % DateFormat(self.added).format("M j")
        raise AttributeError
        
    def needs_more_info(self):
        return not (self.user or (self.first_name and self.email))
        
    def get_full_name(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.email
            
    def __unicode__(self):
        return self.get_full_name()
        
def make_creator_a_guest(sender, instance, **kwargs):
    creator = instance.creator
    Guest.objects.create(event=instance, first_name=creator.first_name, last_name=creator.last_name, 
        email=creator.email, added=datetime.date.today(), is_host=True, user=creator)
models.signals.post_save.connect(make_creator_a_guest, sender=Event)

def notification_on_rsvp(sender, instance, **kwargs):
    if instance.rsvp_status and instance.notify_on_rsvp:
        creator = instance.event.creator
        context = {"user": creator, "guest": instance, "domain": Site.objects.get_current().domain}
        msg = EmailMessage("RSVP from %s to %s" % (instance, instance.event),
            loader.render_to_string("events/rsvp_notify_email.html", context), None, [creator.email])
        msg.content_subtype = "html"
        msg.send()
models.signals.post_save.connect(notification_on_rsvp, sender=Guest)