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

class Points(models.Model):
    """
    Points can be associated with a given action task or a given arbitrarily.
    To assign the points arbitrarily, you should provide a value for `reason`
    
    
    ex: Points(user=request.user, points=10, task=task).save()
    ex: Points(user=request.user, points=10, reason=1).save()
    """
    
    REASONS = (
        (1, "Because we like you"),
        (2, "Because we don't you"),
    )
    
    user = models.ForeignKey(User)
    points = models.IntegerField()
    # TODO Change this to ActionTasks when that model is ready
    task = models.ForeignKey(Action, related_name="task", null=True)
    reason = models.IntegerField(choices=REASONS, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s points' % (self.points)

class Signup(models.Model):
    email = models.EmailField(max_length=255)
    zipcode = models.CharField(max_length=5)

    def __unicode__(self):
        return u'%s' % (self.email)

class Profile(models.Model):
    """Profile"""
    # OPTIMIZE these choices can be tied to an IntegerField if the value is an integer: (1, 'Apartment'),
    BUILDING_CHOICES = (
        ('A', 'Apartment'),
        ('S', 'Single Family Home'),
    )
    user = models.ForeignKey(User, unique=True)
    location = models.ForeignKey(Location, null=True)
    building_type = models.CharField(null=True, max_length=1, choices=BUILDING_CHOICES)
    
    def __unicode__(self):
        return u'%s' % (self.user.username)

    def get_gravatar_url(self):
        return 'http://www.gravatar.com/avatar/%s?r=g&s=200&d=identicon' % (self._email_hash())

    def _email_hash(self):
        return (hashlib.md5(self.user.email.lower()).hexdigest())
