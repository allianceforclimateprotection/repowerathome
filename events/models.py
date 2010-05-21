from django.utils.dateformat import DateFormat

from django.db import models

class Event(models.Model):
    EVENT_TYPES = (
        ("EM", "Energy Meeting",),
        ("CR", "Caulker Rally",),
        ("FT", "Field Training",),
    )

    event_type = models.CharField(max_length=2, choices=EVENT_TYPES)
    where = models.CharField(max_length=100)
    location = models.ForeignKey('geo.Location')
    when = models.DateTimeField()
    details = models.TextField(help_text="For example, where should people park,\
        what's the nearest subway, do people need to be buzzed in, etc.")
    is_private = models.BooleanField()
    
    def __unicode__(self):
        return u"%s in %s, %s" % (self.get_event_type_display(), self.location.name, self.location.st)
    
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
    user = models.ForeignKey("auth.User", null=True, blank=True)
    
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