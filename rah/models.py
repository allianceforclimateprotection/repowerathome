import json
import hashlib
from django.db import models
from django.contrib.auth.models import User as AuthUser
from datetime import datetime
from django.template import Context, loader

import twitter_app.utils as twitter_app

class UserManager(models.Manager):
    def with_completes_for_action(self, action):
        """
        return a 3-tuple query set of user object lists, such that each user object has an additional attribute, completes,
        which identifies how many tasks the user has completed for the given action.
        
        Note: only users that have began completeing task for the action will be listed
        
        The first list in the tuple is for all users that have made progress on the action, the second list is for all users
        that are working on the action (in progress) and the final list is for all users that have completed the action
        """
        total_tasks = action.actiontask_set.all().count()
        users = self.filter(useractiontask__action_task__action=action).annotate(completes=models.Count('useractiontask'))
        in_progress = [user for user in users if total_tasks > user.completes and user.completes > 0]
        completed = [user for user in users if total_tasks == user.completes]

        return (users, in_progress, completed)
        
    def get_user_by_comment(self, comment):
        return self.get(id=comment.user.id)

class User(AuthUser): 
    objects = UserManager()
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
    
    # TODO write unit tests for get latest points
    def get_latest_points(self, quantity=None):
        points = Points.objects.filter(user=self).order_by('task__action' )
        return points[:quantity] if quantity else points
        
    # TODO write unit tests for get total points
    def get_total_points(self):
        return Points.objects.filter(user=self).aggregate(models.Sum('points'))['points__sum']

    # TODO: write unit test for method
    def give_points(self, points, reason):
        """
        Gives a user a certain number of points. Check if we have an int or actiontask instance
        If we have an actiontask, see if we've already given points for it. We don't give double
        points for the same action task.

        OPTIMIZE this seems open to concurrency issues. Maybe lock tables? 
        """
        if type(reason) == ActionTask:
            self.take_points(reason=reason)
            Points(user=self, points=points, task=reason).save()
        else:
            Points(user=self, points=points, reason=reason).save()

    # TODO: write unit test for method
    def take_points(self, reason):
        """Take points away. Used for when a user unchecks an action task. Reason must be an ActionTask"""
        Points.objects.filter(user=self, task=reason).delete()
    
    # TODO: write unit test for method
    def get_chart_data(self):
        from time import mktime
        points       = Points.objects.filter(user=self).order_by('created')
        point_data   = []
        tooltips     = []
        point_tally  = 0
        last_ordinal = None
        
        # Loop through user's recorded points and create data points and tooltips
        # Events are rounded to the nearest day and tooltips are grouped by day
        for point in points:
            point_tally += point.points
            if last_ordinal <> point.created.toordinal():
                rounded_date = mktime(datetime.fromordinal(point.created.toordinal()).timetuple())
                point_data.append([ int(rounded_date) * 1000 - 18000000, point_tally])
                tooltips.append([point])
            else:
                tooltips[len(point_data)-1] += [point]
                point_data[len(point_data)-1][1] = point_tally
                
            last_ordinal = point.created.toordinal()
        
        structured_tooltips = []
        for day in tooltips:
            daytips = {'loose': [], 'actions': {}}
            for p in day:
                if p.reason:
                    daytips['loose'].append(p)
                else:
                    key = str(p.task.action.id)
                    if(key in daytips['actions'].keys()):
                        daytips['actions'][key][1] += [p]
                    else:
                        daytips['actions'][key] = [p.task.action, [p]]
                    
            structured_tooltips.append(daytips)
        
        template = loader.get_template('rah/_chart_tooltip.html')
        rendered_tooltips = []
        for day in structured_tooltips:
             rendered_tooltips.append(template.render(Context(day)))
        
        return json.dumps({"point_data": point_data, "tooltips": rendered_tooltips})

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
        
        the return value is a 4-tuple of action lists; the first values is all the actions,
        the second value is all completed actions, the third value is the in progress actions
        and the last value is the completed actions
        """
        actions = self.select_related().all().extra(
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

        not_complete = [action for action in actions if action.user_completes == 0]
        in_progress = [action for action in actions if action.tasks > action.user_completes and action.user_completes > 0]
        completed = [action for action in actions if action.tasks == action.user_completes]

        return (actions, not_complete, in_progress, completed)

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
    
    # TODO write unit tests for action completes for user
    def completes_for_user(self, user):
        """
        return the number of tasks a user has completed for an action
        """
        return user.useractiontask_set.filter(action_task__action=self).count()
        
    @models.permalink
    def get_absolute_url(self):
        return ('rah.views.action_detail', [str(self.slug)])
        

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
        
    # TODO write unit tests for is action task completed by user
    def is_completed_by_user(self, user):
        """
        return whether or not the specific user has completed the task
        """
        return len(UserActionTask.objects.filter(action_task=self, user=user)) == 1

    # OPTIMIZE pull this static method out and place in a manager
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
    zipcode = models.CharField(max_length=5, db_index=True)
    county = models.CharField(max_length=100, db_index=True)
    st = models.CharField(max_length=2)
    state = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    pop = models.PositiveIntegerField()
    timezone = models.CharField(max_length=100)
    recruit = models.BooleanField()
    
    def __unicode__(self):
        return u'%s, %s (%s)' % (self.name, self.st, self.zipcode)

class Points(DefaultModel):
    """
    Points can be associated with a given action task or a given arbitrarily.
    To assign the points arbitrarily, you should provide an int value for `reason`
    """
    
    REASONS = (
        (1, "You joined Repower@Home"),
        (2, "Because we don't like you"),
    )
    
    class Meta:
        verbose_name_plural = 'points'
    
    user = models.ForeignKey(User)
    points = models.IntegerField()
    task = models.ForeignKey(ActionTask, related_name="task", null=True)
    reason = models.IntegerField(choices=REASONS, null=True)
    
    def get_reason(self):
        return self.task.name if self.task else self.reason
            
    def __unicode__(self):
        return u'%s points' % (self.points)

class Signup(models.Model):
    email = models.EmailField(max_length=255)
    zipcode = models.CharField(max_length=5)

    def __unicode__(self):
        return u'%s' % (self.email)

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
    user = models.ForeignKey(AuthUser, unique=True)
    location = models.ForeignKey(Location, null=True)
    building_type = models.CharField(null=True, max_length=1, choices=BUILDING_CHOICES, blank=True)
    is_profile_private = models.BooleanField(default=0)
    # TODO: does the twitter access token need to be encrypted in the database?
    twitter_access_token = models.CharField(null=True, max_length=255)
    
    def __unicode__(self):
        return u'%s' % (self.user.email)

    # TODO write get_gravatar_url unit test
    def get_gravatar_url(self, default_icon='identicon'):
        return 'http://www.gravatar.com/avatar/%s?r=g&d=%s' % (self._email_hash(), default_icon)

    def _email_hash(self):
        return (hashlib.md5(self.user.email.lower()).hexdigest())
