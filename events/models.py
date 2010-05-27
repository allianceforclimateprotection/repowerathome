import datetime

from django.utils.dateformat import DateFormat

from django.db import models

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
        
    def confirmed_guests(self):
        return Guest.objects.filter(event=self, rsvp_status="A").count()
        
    def outstanding_invitations(self):
        return Guest.objects.filter(event=self, invited__isnull=False, rsvp_status="").count()
    
class Guest(models.Model):
    RSVP_STATUSES = (
        ("A", "Attending",),
        ("M", "Maybe Attending",),
        ("N", "Not Attending",),
    )
    event = models.ForeignKey(Event)
    name = models.CharField(blank=True, max_length=100)
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
        
    def __unicode__(self):
        return self.name if self.name else self.email
        
def make_creator_a_guest(sender, instance, **kwargs):
    creator = instance.creator
    Guest.objects.create(event=instance, name=creator.get_full_name(), email=creator.email, 
        added=datetime.date.today(), is_host=True, user=creator)
models.signals.post_save.connect(make_creator_a_guest, sender=Event)