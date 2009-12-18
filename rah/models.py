import hashlib
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class User(User):
    class Meta:
        proxy = True

    def get_name(self):
        return self.get_full_name() if self.get_full_name() else self.email

    def get_welcome(self):
        return 'Welcome, %s' % (self.get_full_name()) if self.get_full_name() else 'Logged in as, %s' % (self.email)
        
    def set_email(self, email):
        if User.objects.filter(email=email):
            return False
        self.username = hashlib.md5(email).hexdigest()[:30]
        self.email = email
        return True

    def __unicode__(self):
        return u'%s' % (self.email)
    
class DefaultModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return u'%s' % (self.name)

class ActionCat(DefaultModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    teaser = models.TextField()
    content = models.TextField()

class ActionManager(models.Manager):
    def with_tasks_for_user(self, user):
        """
        get a queryset of action objects, the actions will have three additional attributes
        attached: (1)'tasks': the number of tasks related to the action. (2)'user_completes':
        the number of tasks the particular user has completed. (3)'total_points': the number
        of points the action is worth.
        
        each action will also contain a reference to a set of action tasks via the
        'action_tasks' attribute. Each action task in the set will have an additional attribute
        to indicated whether or not the particular user has completed the task, this attribute
        is called 'completed'
        """
        actions = Action.objects.select_related().all().extra(
            select = { 'tasks': 'SELECT COUNT(at.id) \
                                 FROM rah_actiontask at \
                                 WHERE at.action_id = rah_action.id' }).extra(
            select_params = (user.id,),
            select = { 'user_completes': 'SELECT COUNT(uat.id) \
                                          FROM rah_useractiontask uat \
                                          JOIN rah_actiontask at ON uat.action_task_id = at.id \
                                          WHERE uat.user_id = %s AND at.action_id = rah_action.id'}).extra(
            select = { 'total_points': 'SELECT SUM(at.points) \
                                        FROM rah_actiontask at \
                                        WHERE at.action_id = rah_action.id' })

        action_tasks = ActionTask.objects.all().extra(
            select_params = (user.id,), 
            select = { 'completed': 'SELECT rah_useractiontask.completed \
                                     FROM rah_useractiontask \
                                     WHERE rah_useractiontask.user_id = %s AND \
                                     rah_useractiontask.action_task_id = rah_actiontask.id' })
        action_task_dict = dict([(at.id, at) for at in action_tasks])

        for action in actions:
            action.action_tasks = action.actiontask_set.all()
            for action_task in action.action_tasks:
                action_task.completed = action_task_dict[action_task.id].completed

        return actions

class Action(DefaultModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    teaser = models.TextField()
    content = models.TextField()
    category = models.ForeignKey(ActionCat)
    objects = ActionManager()
    
    def get_total_points(self):
        """
        retrieve the summation of all the points in related action tasks
        """
        return self.actiontask_set.aggregate(total=models.Sum('points'))['total']
        
    def get_number_of_tasks(self):
        """
        retrieve the summation of all the points in related action tasks
        """
        return self.actiontask_set.count()
        
    def completes_for_user(self, user):
        """
        return the number of tasks a user has completed for an action
        """
        return user.useractiontask_set.filter(action_task__action=self).count()

class ActionTask(DefaultModel):
    """
    class representing the individual tasks (or steps) a user must complete
    in order to gain successful completion of the associated action
    """
    name = models.CharField(max_length=255)
    content = models.TextField()
    points = models.IntegerField()
    sequence = models.PositiveIntegerField()
    action = models.ForeignKey(Action)
    
    class Meta:
        ordering = ['action', 'sequence']
        unique_together = ('action', 'sequence',)
        
    def is_completed_by_user(self, user):
        """
        return whether or not the specific user has completed the task
        """
        return len(UserActionTask.objects.filter(action_task=self, user=user)) == 1

    @staticmethod
    def get_action_tasks_by_action_and_user(action, user):
        return ActionTask.objects.filter(action=action.id).extra(
            select_params = (user.id,), 
            select = { 'completed': 'SELECT rah_useractiontask.completed \
                                     FROM rah_useractiontask \
                                     WHERE rah_useractiontask.user_id = %s AND \
                                     rah_useractiontask.action_task_id = rah_actiontask.id' })

class UserActionTask(models.Model):
    """
    class representing the ActionTasks a specific user has completed
    """
    action_task = models.ForeignKey(ActionTask)
    user = models.ForeignKey(User)
    completed = models.DateTimeField(auto_now=True)
    
    class Meta:
        get_latest_by = 'complete'

    def __unicode__(self):
        return u'%s completed at %s' % (self.action_task, self.completed)

class Location(models.Model):
    name = models.CharField(max_length=200)
	# OPTIMIZE: adding an index on zipcode should speed up the searches
    zipcode = models.CharField(max_length=5)
    county = models.CharField(max_length=100)
    st = models.CharField(max_length=2)
    state = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    pop = models.PositiveIntegerField()
    timezone = models.CharField(max_length=100)
    
    def __unicode__(self):
        return u'%s, %s (%s)' % (self.name, self.st, self.zipcode)

class Points(DefaultModel):
    """
    Points can be associated with a given action task or a given arbitrarily.
    To assign the points arbitrarily, you should provide an int value for `reason`
    """
    
    REASONS = (
        (1, "Because we like you"),
        (2, "Because we don't like you"),
    )
    
    class Meta:
        verbose_name_plural = 'points'
    
    user = models.ForeignKey(User)
    points = models.IntegerField()
    task = models.ForeignKey(ActionTask, related_name="task", null=True)
    reason = models.IntegerField(choices=REASONS, null=True)
    
    # TODO: write unit test for give method
    @staticmethod
    def give(points, reason, user):
        """
        Gives a user a certain number of points. Check if we have an int or actiontask instance
        If we have an actiontask, see if we've already given points for it. We don't give double
        points for the same action task.
        
        OPTIMIZE this seems open to concurrency issues. Maybe lock tables? 
        """
        if type(reason) == ActionTask:
            Points.take(user=user, reason=reason)
            Points(user=user, points=points, task=reason).save()
        else:
            Points(user=user, points=points, reason=reason).save()

    # TODO: write unit test for take method
    @staticmethod
    def take(user, reason):
        """Take points away. Used for when a user unchecks an action task. Reason must be an ActionTask"""
        Points.objects.filter(user=user, task=reason).delete()
        
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
    building_type = models.CharField(null=True, max_length=1, choices=BUILDING_CHOICES, blank=True)
    is_profile_private = models.BooleanField(default=0)
    
    def __unicode__(self):
        return u'%s' % (self.user.username)

    # TODO write get_gravatar_url unit test
    def get_gravatar_url(self, size=200, default_icon='identicon'):
        return 'http://www.gravatar.com/avatar/%s?r=g&s=%s&d=%s' % (self._email_hash(), size, default_icon)

    def _email_hash(self):
        return (hashlib.md5(self.user.email.lower()).hexdigest())
