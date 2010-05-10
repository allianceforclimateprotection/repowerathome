import random
import hashlib
from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site

from records.models import Record

"""
u = User.objects.get(pk=1)
g = Group.objects.get(pk=1)
Invitation.objects.invite(u, "jonlesser@gmail.com", "some_type", [content_object])

"""
class InvitationManager(models.Manager):            
    def make_token(self):
        token = hashlib.sha1("%s %s" % (random.random(), datetime.now())).hexdigest()
        return token[:15]

class Invitation(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=255)
    token = models.CharField(max_length=15)
    content_type = models.ForeignKey(ContentType, verbose_name="content type", related_name="%(class)s", 
        null=True, blank=True)
    object_pk = models.PositiveIntegerField("object ID", null=True, blank=True)
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    objects = InvitationManager()
    
    class Meta:
        unique_together = (('token',))
    
    @models.permalink
    def get_absolute_url(self):
        return ('invite.views.rsvp', [self.token])
    
    def get_permalink(self):
        return "http://%s%s" % (Site.objects.get_current(), self.get_absolute_url())

class Rsvp(models.Model):
    invitee = models.ForeignKey(User)
    invitation = models.ForeignKey(Invitation)
    created = models.DateTimeField(auto_now_add=True)
    
def record_user_invitation_accepted(sender, instance, **kwargs):
    Record.objects.create_record(instance.invitation.user, 'mag_invite_friend')
models.signals.post_save.connect(record_user_invitation_accepted, sender=Rsvp)