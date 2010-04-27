from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink
import random
import hashlib
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site

"""
u = User.objects.get(pk=1)
g = Group.objects.get(pk=1)
Invitation.objects.invite(u, "jonlesser@gmail.com", "some_type", [content_object])

"""

class InvitationManager(models.Manager):
    def invite(self, user, email, invite_type, content_id=None):
        return Invitation.objects.create(user=user, email=email, invite_type=invite_type, 
            content_id=content_id, token=self.make_token())
    
    def rsvp(self, invitee, invitation):
        rsvp, created = Rsvp.objects.get_or_create(invitee=invitee, invitation=invitation)
        return rsvp if created else None
    
    def make_token(self):
        token = hashlib.sha1("%s %s" % (random.random(), datetime.now())).hexdigest()
        return token[:15]

class Invitation(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=255)
    token = models.CharField(max_length=15)
    content_id = models.IntegerField(null=True)
    invite_type = models.CharField(max_length=255)
    objects = InvitationManager()
    
    class Meta:
        unique_together = (('token',))
    
    @models.permalink
    def get_absolute_url(self):
        return ('invite.views.invite_welcome', [self.token])
    
    def get_permalink(self):
        return "http://%s%s?next=%s" % (Site.objects.get_current(), reverse("login"), self.get_absolute_url())

class Rsvp(models.Model):
    invitee = models.ForeignKey(User)
    invitation = models.ForeignKey(Invitation)
    created = models.DateTimeField(auto_now_add=True)
