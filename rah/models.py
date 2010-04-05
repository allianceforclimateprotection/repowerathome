import json, hashlib, re
from django.db import models
from django.contrib.auth.models import User as AuthUser

from geo.models import Location
from records.models import Record
from twitter_app import utils as twitter_app
from actions.models import UserActionProgress

class DefaultModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % (self.name)

class User(AuthUser):
    class Meta:
        proxy = True

    def set_action_commitment(self, action, date_committed):
        """date_committed can be set to None to remove a commitment"""
        uap = UserActionProgress.objects.filter(action=action, user=self)
        if uap:
            row = uap[0]
            row.date_committed = date_committed
            row.save()
        else:
            row = UserActionProgress(action=action, user=self, date_committed=date_committed).save()
        return row
    
    def get_action_progress(self, action):
        try:
            return UserActionProgress.objects.get(action=action, user=self)
        except UserActionProgress.DoesNotExist: pass
        return None
    
    def get_commit_list(self):
        return UserActionProgress.objects.select_related().filter(user=self, is_completed=0, date_committed__isnull=False).order_by("date_committed")
        
    def __unicode__(self):
        return u'%s' % (self.get_full_name())
    

class Signup(models.Model):
    email = models.EmailField(max_length=255)
    zipcode = models.CharField(max_length=5)

    def __unicode__(self):
        return u'%s' % (self.email)

class Feedback(DefaultModel):
    user = models.ForeignKey(AuthUser, null=True)
    url = models.CharField(max_length=255, default='')
    comment = models.TextField(default='')
    beta_group = models.BooleanField(default=0)

    def __unicode__(self):
        return u'%s...' % (self.comment[:15])

class Profile(models.Model):
    """Profile"""
    # OPTIMIZE these choices can be tied to an IntegerField if the value is an integer: (1, 'Apartment'),
    BUILDING_CHOICES = (
        ('A', 'Apartment'),
        ('S', 'Single Family Home'),
    )

    user = models.ForeignKey(AuthUser, unique=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    building_type = models.CharField(null=True, max_length=1, choices=BUILDING_CHOICES, blank=True)
    about = models.CharField(null=True, blank=True, max_length=255)
    is_profile_private = models.BooleanField(default=0)
    twitter_access_token = models.CharField(null=True, max_length=255, blank=True)
    total_points = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u'%s' % (self.user.email)

    def get_gravatar_url(self, default_icon='identicon'):
        return 'http://www.gravatar.com/avatar/%s?r=g&d=%s' % (self._email_hash(), default_icon)

    def _email_hash(self):
        return (hashlib.md5(self.user.email.lower()).hexdigest())

"""
SIGNALS!
"""
def user_post_save(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)
    
models.signals.post_save.connect(user_post_save, sender=AuthUser)
models.signals.post_save.connect(user_post_save, sender=User)