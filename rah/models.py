import hashlib

from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

class Action(models.Model):
    name = models.CharField(max_length=255)
    teaser = models.TextField()
    content = models.TextField()
    points = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('ActionCat')
    status = models.ManyToManyField(User, through='ActionStatus')
    
    def __unicode__(self):
        return u'%s' % (self.name)
    

class ActionCat(models.Model):
    name = models.CharField(max_length=255)
    teaser = models.TextField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
class ActionStatus(models.Model):
    user = models.ForeignKey(User)
    action = models.ForeignKey(Action)
    status = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % (self.status)
        
class Profile(models.Model):
    """Profile"""
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return u'%s' % (self.user.username)
        
    def get_gravatar_url(self):
        return 'http://www.gravatar.com/avatar/%s?d=identicon' % (hashlib.md5(self.user.email.lower()).hexdigest())
        