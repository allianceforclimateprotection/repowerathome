import json
import hashlib
import re

from django.db import models
from django.contrib.auth.models import User

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

class Feedback(DefaultModel):
    user = models.ForeignKey(User, null=True)
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

    user = models.ForeignKey(User, unique=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    building_type = models.CharField(null=True, max_length=1, choices=BUILDING_CHOICES, blank=True)
    about = models.CharField(null=True, blank=True, max_length=255)
    is_profile_private = models.BooleanField(default=0)
    twitter_access_token = models.CharField(null=True, max_length=255, blank=True)
    total_points = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u'%s' % (self.user.email)

    def get_gravatar_url(self, default_icon='identicon'):
        return 'http://www.gravatar.com/avatar/%s?r=g&d=%s&s=52' % (self._email_hash(), default_icon)
    
    def get_gravatar_url_large(self, default_icon='identicon'):
        # TODO: Write unit test for get_gravatar_url_large
        return 'http://www.gravatar.com/avatar/%s?r=g&d=%s&s=189' % (self._email_hash(), default_icon)

    def _email_hash(self):
        return (hashlib.md5(self.user.email.lower()).hexdigest())
        
    def potential_points(self):
        return UserActionProgress.objects.filter(user=self.user, date_committed__isnull=False, 
            is_completed=0).aggregate(models.Sum("action__points"))["action__points__sum"]

"""
SIGNALS!
"""
def user_post_save(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)
    
models.signals.post_save.connect(user_post_save, sender=User)