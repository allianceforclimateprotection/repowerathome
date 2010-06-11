import datetime

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.db import models
from django.dispatch import Signal
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
    duration = models.PositiveIntegerField(blank=True, null=True)
    details = models.TextField(help_text="For example, where should people park,\
        what's the nearest subway, do people need to be buzzed in, etc.", blank=True)
    is_private = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = (
            ("host_any_event_type", "Can host any event type"),
        )
    
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
        
    def attendees(self):
        return Guest.objects.filter(event=self, rsvp_status="A")
        
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
        
class GuestManager(models.Manager):
    def create_or_update(self, *args, **kwargs):
        pass
        
class Guest(models.Model):
    RSVP_STATUSES = (
        ("A", "Attending",),
        ("M", "Maybe Attending",),
        ("N", "Not Attending",),
    )
    event = models.ForeignKey(Event)
    first_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(blank=True, max_length=50)
    email = models.EmailField(blank=True, db_index=True)
    phone = models.CharField(blank=True, max_length=12)
    invited = models.DateField(null=True, blank=True)
    added = models.DateField(null=True, blank=True)
    rsvp_status = models.CharField(blank=True, max_length=1, choices=RSVP_STATUSES)
    notify_on_rsvp = models.BooleanField(default=False)
    is_host = models.BooleanField(default=False)
    user = models.ForeignKey("auth.User", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = (("event", "email",),("event", "user",),)
        
    def _set_name(self, value):
        first, space, last = value.partition(" ")
        self.first_name = first
        self.last_name = last
    def _get_name(self):
        return ("%s %s" % (self.first_name, self.last_name)).strip()
    name = property(_get_name, _set_name)
    
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
        if self.user:
            return self.user.get_full_name()
        elif self.name:
            return self.name
        else:
            return self.email
            
    def __unicode__(self):
        return self.get_full_name()
        
class Survey(models.Model):
    name = models.CharField(max_length=50, unique=True)
    event_type = models.ForeignKey(EventType)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Survey for %s" % self.event_type
        
class Challenge(models.Model):
    name = models.CharField(max_length=100)
    survey = models.ForeignKey(Survey)
    order = models.PositiveIntegerField()
    action = models.ForeignKey("actions.Action", null=True)
    guests = models.ManyToManyField(Guest, through="Commitment")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = (("survey", "order",),)
    
    def __unicode__(self):
        return self.name
        
class Commitment(models.Model):
    ANSWERS = (
        ("P", "Will Do"),
        ("D", "Already Done"),
    )
    
    guest = models.ForeignKey(Guest, db_index=True)
    challenge = models.ForeignKey(Challenge, db_index=True)
    answer = models.CharField(choices=ANSWERS, max_length=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = (("guest", "challenge"),)
    
def make_creator_a_guest(sender, instance, **kwargs):
    creator = instance.creator
    Guest.objects.get_or_create(event=instance, user=creator, defaults={"first_name":creator.first_name, 
        "last_name":creator.last_name, "email":creator.email, "added":datetime.date.today(), 
        "rsvp_status": "A", "is_host":True})
models.signals.post_save.connect(make_creator_a_guest, sender=Event)

rsvp_recieved = Signal(providing_args=["guest"])
def notification_on_rsvp(sender, guest, **kwargs):
    if guest.rsvp_status and guest.notify_on_rsvp:
        creator = guest.event.creator
        context = {"user": creator, "guest": guest, "domain": Site.objects.get_current().domain}
        msg = EmailMessage("RSVP from %s to %s" % (guest, guest.event),
            loader.render_to_string("events/rsvp_notify_email.html", context), None, [creator.email])
        msg.content_subtype = "html"
        msg.send()
rsvp_recieved.connect(notification_on_rsvp)

def link_guest_to_user(sender, instance, **kwargs):
    if instance.email:
        try:
            user = User.objects.get(email=instance.email)
            instance.user = user
        except User.DoesNotExist:
            instance.user = None
models.signals.pre_save.connect(link_guest_to_user, sender=Guest)