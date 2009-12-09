import hashlib
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Action(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    teaser = models.TextField()
    content = models.TextField()
    points = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('ActionCat')
        
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

class ActionTask(models.Model):
    """
    class representing the individual tasks (or steps) a user must complete
    in order to gain successful completion of the associated action
    """
    action = models.ForeignKey(Action)
    name = models.CharField(max_length=255)
    content = models.TextField()
    sequence = models.PositiveIntegerField()
    
    def __unicode__(self):
        return u'%s' % (self.name)

class UserActionTask(models.Model):
    """
    class representing the ActionTasks a specific user has completed
    """
    task = models.ForeignKey(ActionTask)
    user = models.ForeignKey(User)
    completed = models.DateTimeField(blank=True, default=datetime.now)

    def __unicode__(self):
        return u'%s completed at %s' % (self.task, self.completed)

    @classmethod
    def get_tasks_by_user_action_with_default(clas, action, user):
        """docstring for get_tasks_by_user_action_with_default"""
        from django.db import connection, transaction
        cursor = connection.cursor()
        query = """
            SELECT at.name, at.content, at.sequence, uat.completed
            FROM rah_useractiontask uat
            RIGHT JOIN rah_actiontask at ON uat.task_id = at.id AND uat.user_id = %s
            WHERE at.action_id = %s
        """
        cursor.execute(query, [user.id, action.id])
        rows = cursor.fetchall()
        user_action_tasks = []
        for row in rows:
            task = ActionTask(action=action, name=row[0], content=row[1], sequence=row[2])
            user_action_tasks.append(UserActionTask(task=task, user=user, completed=row[3]))
        return user_action_tasks

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
