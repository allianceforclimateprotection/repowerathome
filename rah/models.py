import json, hashlib, time, base64
from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from datetime import datetime, timedelta
from django.template import Context, loader

try:
    import cPickle as pickle
except:
    import pickle

import twitter_app.utils as twitter_app

class SerializedDataField(models.TextField):
    """Because Django for some reason feels its needed to repeatedly call
    to_python even after it's been converted this does not support strings."""
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value is None: return
        if not isinstance(value, basestring): return value
        value = pickle.loads(base64.b64decode(value))
        return value

    def get_db_prep_save(self, value):
        if value is None: return
        return base64.b64encode(pickle.dumps(value))

class DefaultModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return u'%s' % (self.name)

class ChartPoint(object):
    """docstring for ChartPoint"""
    def __init__(self, date):
        super(ChartPoint, self).__init__()
        self.date = date
        self.points = 0
        self.records = []
        
    def add_record(self, record):
        if self.date == record.created.date():
            self.records.append(record)
        self.points += record.points
        
    def get_date_as_milli_from_epoch(self):
        return (int(time.mktime(self.date.timetuple())) - 18000) * 1000
        
    def __unicode__(self):
        return u"(%s, %s) with %s" % (self.date, self.points, self.records)
        
    def __str__(self):
        return unicode(self).encode('utf-8')
        
    def __repr__(self):
        return u'<%s: %s>' % (self.__class__.__name__, unicode(self))
        
    def __cmp__(self, other):
        return cmp(self.date, other.date)
        
    def __hash__(self):
        return hash(self.date)
        
class User(AuthUser):
    class Meta:
        proxy = True

    def get_name(self):
        return self.get_full_name() if self.get_full_name() else "Repower@Home User"

    def get_latest_records(self, quantity=None):
        records = self.record_set.filter(void=False)
        return records[:quantity] if quantity else records

    def record_activity(self, activity, content_object=None, data=None):
        if type(activity) is str:
            activity = Activity.objects.get(slug=activity)
        
        # Figure out how many points we're going to give.
        points = content_object.points if hasattr(content_object, "points") else activity.points
        
        # Add a new content_object (and don't create a new record) if this is batachable
        if activity.batch_time_minutes and content_object:
            # see if one exists in timeframe
            batch_minutes = activity.batch_time_minutes
            cutoff_time = datetime.now()-timedelta(minutes=batch_minutes)
            batchable_items = Record.objects.filter(user=self, activity=activity, 
                                                    created__gt=cutoff_time).order_by('-created').all()[0:1]

            if batchable_items:
                batchable_items[0].content_objects.create(content_object=content_object)
                batchable_items[0].is_batched = True
                batchable_items[0].points += points
                batchable_items[0].save()
                return batchable_items[0]

        record = Record.objects.create(user=self, activity=activity, data=data, points=points)
        if content_object: record.content_objects.create(content_object=content_object)
        record.save()
        return record

    def unrecord_activity(self, activity, content_object):
        if type(activity) is str:
            activity = Activity.objects.get(slug=activity)
        record = Record.objects.filter(void=False, user=self, activity=activity, content_objects__object_id=content_object.id)[0:1]
        if record:
            record[0].void = True
            record[0].save()

    def get_chart_data(self):
        records = self.get_latest_records().select_related().order_by("created")
        chart_points = list(sorted(set([ChartPoint(record.created.date()) for record in records])))
        for chart_point in chart_points:
            [chart_point.add_record(record) for record in records if chart_point.date >= record.created.date()]

        return chart_points

    def set_action_commitment(self, action, date_committed):
        uap = UserActionProgress.objects.filter(action=action, user=self)
        if uap:
            row = uap[0]
            row.date_committed = date_committed
            row.save()
        else:
            row = UserActionProgress(action=action, user=self, date_committed=date_committed).save()
        return row
    
    def get_action_progress(self, action):
        uap = UserActionProgress.objects.filter(action=action, user=self)
        return uap[0] if uap else None
    
    def get_commit_list(self):
        return UserActionProgress.objects.select_related().filter(user=self, is_completed=0, date_committed__isnull=False).order_by("date_committed")
    
    def __unicode__(self):
        return u'%s' % (self.email)
        
class Group(DefaultModel):
    MEMBERSHIP_CHOICES = (
        ('O', 'Open membership'),
        ('C', 'Closed membership'),
    )
    
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    membership_type = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default="O")
    image = models.ImageField(upload_to="group_images", null=True)
    is_featured = models.BooleanField(default=False)
    users = models.ManyToManyField(User, through="GroupUsers")
    
    def join(self, user):
        if self.membership_type == "O":
             GroupUsers.objects.create(group=self, user=user, is_manager=False)
        return True
    
    def completed_actions_by_user(self):
        """
        what actions have been completed by users in this group and how many users have completed each action
        """
        actions = Action.objects.filter(useractionprogress__user__group=self, useractionprogress__is_completed=1)
        return actions.annotate(users_completed=models.Count("useractionprogress__is_completed"))
        
    def members_ordered_by_points(self, limit=None):
        users = User.objects.filter(group=self)
        users = users.annotate(actions_completed=models.Sum("useractionprogress__is_completed"))
        users = users.annotate(last_active=models.Max("record__created"))
        users = list(users[:limit]) if limit else list(users)
        users.sort(lambda x,y: int(y.get_profile().total_points - x.get_profile().total_points))
        return users
        
    def group_records(self, limit=None):
        records = Record.objects.filter(user__group=self).order_by("created")
        records = records[:limit] if limit else records
        return records

class GroupUsers(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    is_manager = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%s belongs to group %s' % (self.user, self.group)

class ActionCat(DefaultModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    teaser = models.TextField()
    content = models.TextField()
    
class ActionManager(models.Manager):
    # TODO: Write unit test for actions_by_completion_status
    def actions_by_completion_status(self, user):
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
        actiontasks = ActionTask.objects.select_related().all().extra(
            select_params = (user.id,), 
            select = { 'completed': 'SELECT rah_actiontaskuser.created \
                                     FROM rah_actiontaskuser \
                                     WHERE rah_actiontaskuser.user_id = %s AND \
                                     rah_actiontaskuser.actiontask_id = rah_actiontask.id'})
                                     
        action_dict = dict([actiontask.action, []] for actiontask in actiontasks)
        [action_dict[actiontask.action].append(actiontask) for actiontask in actiontasks]
        for action, actiontasks in action_dict.items():
            action.user_completes = 0
            action.actiontasks = actiontasks
            for actiontask in actiontasks:
                action.user_completes += 1 if actiontask.completed else 0
        actions = action_dict.keys()

        not_complete = [action for action in actions if action.user_completes == 0]
        in_progress = [action for action in actions if action.total_tasks > action.user_completes and action.user_completes > 0]
        completed = [action for action in actions if action.total_tasks == action.user_completes]
        return (actions, not_complete, in_progress, completed)

class Action(DefaultModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    teaser = models.TextField()
    content = models.TextField()
    total_tasks = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    users_in_progress = models.IntegerField(default=0)
    users_completed = models.IntegerField(default=0)
    users_committed = models.IntegerField(default=0)
    category = models.ForeignKey(ActionCat)
    users = models.ManyToManyField(User, through="UserActionProgress")
    objects = ActionManager()
    
    def completes_for_user(self, user):
        """
        return the number of tasks a user has completed for an action
        """
        uap = UserActionProgress.objects.filter(action=self, user=user)[0:1]
        return uap[0].user_completes if uap else 0
        
    def users_with_completes(self, limit=5):
        in_progress = UserActionProgress.objects.select_related().filter(action=self, is_completed=0)[:limit]
        completed = UserActionProgress.objects.select_related().filter(action=self, is_completed=1)[:limit]
        
        return (self.users_in_progress, [uap.user for uap in in_progress], self.users_completed, [uap.user for uap in completed])
        
    def get_action_tasks_by_user(self, user):
        return ActionTask.objects.filter(action=self).extra( select_params = (user.id,), 
                select = { 'is_complete': 'SELECT rah_actiontaskuser.created \
                                           FROM rah_actiontaskuser \
                                           WHERE rah_actiontaskuser.user_id = %s AND \
                                           rah_actiontaskuser.actiontask_id = rah_actiontask.id' })
        
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
    sequence = models.PositiveIntegerField()
    action = models.ForeignKey(Action)
    points = models.IntegerField(default=0)
    users = models.ManyToManyField(User, through="ActionTaskUser")

    class Meta:
        ordering = ['action', 'sequence']
        unique_together = ('action', 'sequence',)
    
    def complete_task(self, user, undo=False):
        if undo:
            ActionTaskUser.objects.filter(user=user, actiontask=self).delete()
        else:
            ActionTaskUser(user=user, actiontask=self).save()
        
        # Maintain denomed columns on Action and UserActionProgress 
        action = self.action
        obj, created = UserActionProgress.objects.get_or_create(user=user, action=action)
        new_completes = obj.user_completes + 1 if not undo else obj.user_completes - 1
        new_completed = 1 if new_completes >= action.total_tasks else 0
        inprogress = 1  if obj.is_completed != 1 and obj.user_completes > 0 else 0 # the useraction is currently in_progress if it is not completed, but the completes count is greater than 0
        new_inprogress = 1 if new_completed != 1 and new_completes > 0 else 0 # the useraction is going to be in_progress if it will not be completed, but the new completes count is greater than 0
        
        if obj.is_completed != new_completed:
            action.users_completed += new_completed - obj.is_completed
        if inprogress != new_inprogress:
            action.users_in_progress += new_inprogress - inprogress
        if obj.is_completed != new_completed or inprogress != new_inprogress:
            action.save()
        
        obj.user_completes = new_completes
        obj.is_completed = new_completed
        obj.save()

class ActionTaskUser(DefaultModel):
    actiontask = models.ForeignKey(ActionTask)
    user = models.ForeignKey(User)
    
    class Meta:
        unique_together = ('actiontask', 'user',)
    
    def __unicode__(self):
        return "yes"
        # return "User: %s, ActionTask: %s" % (self.user.id, self.actiontask.sequence)

class UserActionProgress(models.Model):
    user = models.ForeignKey(User)
    action = models.ForeignKey(Action)
    user_completes = models.IntegerField(default=0)
    is_completed = models.IntegerField(default=0)
    date_committed = models.DateField(null=True)
    
    def __unicode__(self):
        return "(%s, %s) has %s complete(s) and is%scompleted" % (self.user, self.action, self.user_completes, (" " if self.is_completed else " not "))

class Location(models.Model):
    name = models.CharField(max_length=200)
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


class Activity(DefaultModel):
    """
    _Jon_ earned _10_ points for _installing a low-flow shower head_
    _Jon_ committed to _install a low flow shower head_ on _Feb. 5th_

    <a href="{{ user.permalink }}">{{ user.get_name }}</a> committed 
    to _install a low flow shower head_ on {{ date_committted }}

    {
        "user": user_id,
        "user": user.get_name,
        "date_"committed: date_committed
    }
    """
    slug = models.SlugField()
    points = models.IntegerField(default=0)
    users = models.ManyToManyField(User, through="Record")
    batch_time_minutes = models.IntegerField("batch time in minutes", default=0, blank=True)
    
    def __unicode__(self):
        return u'%s' % (self.slug)

class Record(DefaultModel):
    user = models.ForeignKey(User)
    activity = models.ForeignKey(Activity)
    points = models.IntegerField(default=0)
    data = SerializedDataField(blank=True, null=True)
    is_batched = models.BooleanField(default=False)
    void = models.BooleanField(default=False)
    # cos = generic.GenericRelation("RecordActivityObject", related_name="content_object")

    class Meta:
        ordering = ["user", "activity", "created"]
        get_latest_by = "created"

    def render(self):
        if self.is_batched:
            template_file = "activity/%s_batch.html" % self.activity.slug
        else:
            template_file = "activity/%s.html" % self.activity.slug
        template = loader.get_template(template_file)
        content_object = self.content_objects.get().content_object
        return template.render(Context({"record": self, "content_object":content_object}))

    def __unicode__(self):
        return "user: %s, activity: %s" % (self.user, self.activity)

class RecordActivityObject(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    record = models.ForeignKey(Record, related_name="content_objects")
    
    class Meta:
        unique_together = ('content_type', 'object_id', 'record',)
    
    def __unicode__(self):
        return "%s %s" % (self.content_type, self.object_id)

"""
SIGNALS!
"""
def update_actiontask_counts(sender, instance, **kwargs):
    instance.action.total_tasks = ActionTask.objects.filter(action=instance.action).count()
    instance.action.total_points = ActionTask.objects.filter(action=instance.action).aggregate(models.Sum('points'))['points__sum']
    instance.action.save()
        
def user_post_save(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)

def update_profile_points(sender, instance, **kwargs):
    if instance.points == 0: return
    profile = instance.user.get_profile()
    total_points = Record.objects.filter(user=instance.user, void=False).aggregate(models.Sum('points'))['points__sum']
    profile.total_points = total_points if total_points else 0
    profile.save()

models.signals.post_save.connect(update_actiontask_counts, sender=ActionTask)
models.signals.pre_delete.connect(update_actiontask_counts, sender=ActionTask)
models.signals.post_save.connect(user_post_save, sender=User)
models.signals.post_save.connect(update_profile_points, sender=Record)