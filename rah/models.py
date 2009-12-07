import hashlib
from django.db import models
from django.contrib.auth.models import User

class Action(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
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
    slug = models.CharField(max_length=255)
    teaser = models.TextField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
class ActionStatus(models.Model):
    STATUS_CHOICES = (
        ('Committed', 'Committed'),
        ('Finished', 'Finished'),
    )
    
    user = models.ForeignKey(User)
    action = models.ForeignKey(Action)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s (%s), %s (%s), %s' % (self.user.username, self.user.id, self.action.name,
                                          self.action.id, self.status)

class Location(models.Model):
    name = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=5)
    county = models.CharField(max_length=100)
    st = models.CharField(max_length=2)
    state = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    pop = models.PositiveIntegerField()
    timezone = models.CharField(max_length=100)
    
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.zipcode)

class Signup(models.Model):
    email = models.EmailField(max_length=255)
    zipcode = models.CharField(max_length=5)

    def __unicode__(self):
        return u'%s' % (self.email)

class Profile(models.Model):
    """Profile"""
    user = models.ForeignKey(User, unique=True)
    location = models.ForeignKey(Location, null=True)

    def __unicode__(self):
        return u'%s' % (self.user.username)

    def get_gravatar_url(self):
        return 'http://www.gravatar.com/avatar/%s?r=g&s=200&d=identicon' % (self._email_hash())

    def _email_hash(self):
        return (hashlib.md5(self.user.email.lower()).hexdigest())
