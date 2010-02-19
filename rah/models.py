import json, hashlib, time, re
from django.db import models
from django.contrib.auth.models import User as AuthUser
from datetime import datetime, timedelta
from geo.models import Location

import twitter_app.utils as twitter_app

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
        
    def is_group_manager(self, group):
        return GroupUsers.objects.filter(user=self, group=group, is_manager=True).exists()
        
    def my_groups(self):
        groups = list(Group.objects.filter(users=self))
        return groups + GeoGroup.objects.get_users_geo_groups(self)
        
    def __unicode__(self):
        return u'%s' % (self.get_full_name())
        
class BaseGroup(object):
    _must_redefine = Exception("Implementation of BaseGroup must redefine this method")
    
    def is_joinable(self):
        raise _must_redefine
        
    def is_member(self):
        raise _must_redefine
        
    def _group_users_filtered(self):
        raise _must_redefine
        
    def _group_actions_filtered(self):
        raise _must_redefine
        
    def _group_records_filtered(self):
        raise _must_redefine
        
    def is_public(self):
        return True
        
    def completed_actions_by_user(self):
        """
        what actions have been completed by users in this group and how many users have completed each action
        """
        actions = self._group_actions_filtered()
        actions = actions.order_by("-users_completed")
        actions = actions.filter(useractionprogress__is_completed=1)
        actions = actions.annotate(users_completed=models.Count("useractionprogress__is_completed"))
        return actions
        
    def members_ordered_by_points(self, limit=None):
        users = self._group_users_filtered()
        users = users.order_by("-profile__total_points")
        users = users.annotate(actions_completed=models.Sum("useractionprogress__is_completed"))
        users = users.annotate(actions_committed=models.Count("useractionprogress__date_committed"))
        return users[:limit] if limit else users
        
    def group_records(self, limit=None):
        records = self._group_records_filtered()
        records = records.select_related().order_by("-created")
        return records[:limit] if limit else records
        
    def has_pending_membership(self, user):
        return False
        
    def requesters_to_grant_or_deny(self, user):
        return []
        
class Group(DefaultModel, BaseGroup):
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
    requesters = models.ManyToManyField(User, through="MembershipRequests", related_name="requested_group_set")
    
    def is_joinable(self):
        return True
    
    def is_public(self):
        return self.membership_type == "O"
        
    def is_member(self, user):
        if user.is_authenticated():
            return GroupUsers.objects.filter(group=self, user=user).exists()
        return False
        
    def _group_users_filtered(self):
        return User.objects.filter(group=self)

    def _group_actions_filtered(self):
        return Action.objects.filter(useractionprogress__user__group=self)

    def _group_records_filtered(self):
        # TODO: puposely broken for now
        return 
        return Record.objects.filter(user__group=self)
    
    def has_pending_membership(self, user):
        if user.is_authenticated():
            return MembershipRequests.objects.filter(group=self, user=user).exists()
        return False
        
    def requesters_to_grant_or_deny(self, user):
        if user.is_authenticated() and user.is_group_manager(self):
            return User.objects.filter(membershiprequests__group=self)
        return []
        
    @models.permalink
    def get_absolute_url(self):
        return ("group_detail", [str(self.slug)])
        
class GeoGroupManager(models.Manager):    
    def geo_slugify(self, value):
        return re.sub("[\s]", "-", value).lower()

    def de_geo_slugify(self, value):
        return re.sub("[-]", " ", value).title()
    
    def get_geo_group(self, state, county_slug=None, place_slug=None):
        locations = Location.objects.filter(st=state)
        if place_slug:
            place = self.de_geo_slugify(place_slug)
            locations = locations.filter(name=place)
        elif county_slug:
            county = self.de_geo_slugify(county_slug)
            locations = locations.filter(county=county)
        
        if locations.count() == 0:
            return None
            
        return GeoGroup(locations=locations, state=state, county_slug=county_slug, place_slug=place_slug)
            
    def get_users_geo_groups(self, user):
        location = user.get_profile().location
        if location:
            state = location.st
            county_slug = self.geo_slugify(location.county)
            place_slug = self.geo_slugify(location.name)
            return [self.get_geo_group(state),
                        self.get_geo_group(state, county_slug),
                        self.get_geo_group(state, county_slug, place_slug),]
        return []
        
class GeoGroup(BaseGroup):
    objects = GeoGroupManager()
    
    class Meta:
        managed = False
        
    def __init__(self, locations, state, county_slug=None, place_slug=None, *args, **kwargs):
        self.locations = locations
        self.state = state
        self.county_slug = county_slug
        self.place_slug = place_slug
        self._set_attributes(locations[0], county_slug != None, place_slug != None)
        
    def _set_attributes(self, location, has_county, has_place):
        if has_place:
            self.name = "%s, %s" % (location.name, location.st)
        elif has_county:
            self.name = "%s in %s" % (location.county, location.state)
        else:
            self.name = location.state
        self.description = "A meeting place for all users belonging to %s" % self.name
        self.image = "geo_group_images/geo.jpg"
        
    def is_joinable(self):
        return False 
        
    def is_public(self):
        return True

    def is_member(self, user):
        if user.is_authenticated():
            return User.objects.filter(pk=user.id, profile__location__in=self.locations).exists()
        return False

    def _group_users_filtered(self):
        return User.objects.filter(profile__location__in=self.locations)

    def _group_actions_filtered(self):
        return Action.objects.filter(useractionprogress__user__profile__location__in=self.locations)

    def _group_records_filtered(self):
        # TODO: Purposely broken for now
        return
        return Record.objects.filter(user__profile__location__in=self.locations)
        
    @models.permalink
    def get_absolute_url(self):
        if self.place_slug:
            return ("geo_group_place", [self.state, self.county_slug, self.place_slug])
        elif self.county_slug:
            return ("geo_group_county", [self.state, self.county_slug])
        return ("geo_group_state", [self.state])

class GroupUsers(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    is_manager = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%s belongs to group %s' % (self.user, self.group)
        
class MembershipRequests(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s request to join %s on %s' % (self.user, self.group, self.created)

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
        return u"User: %s, ActionTask: %s" % (self.user.id, self.actiontask.sequence)

class UserActionProgress(models.Model):
    user = models.ForeignKey(User)
    action = models.ForeignKey(Action)
    user_completes = models.IntegerField(default=0)
    is_completed = models.IntegerField(default=0)
    date_committed = models.DateField(null=True)
    
    def __unicode__(self):
        return u"(%s, %s) has %s complete(s) and is%scompleted" % (self.user, self.action, self.user_completes, (" " if self.is_completed else " not "))

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

"""
SIGNALS!
"""
def update_actiontask_counts(sender, instance, **kwargs):
    instance.action.total_tasks = ActionTask.objects.filter(action=instance.action).count()
    instance.action.total_points = ActionTask.objects.filter(action=instance.action).aggregate(models.Sum('points'))['points__sum']
    instance.action.save()
        
def user_post_save(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)

def update_commited_action(sender, instance, **kwargs):
    instance.action.users_committed = UserActionProgress.objects.filter(action=instance.action, date_committed__isnull=False).count()
    instance.action.save()

models.signals.post_save.connect(update_actiontask_counts, sender=ActionTask)
models.signals.post_delete.connect(update_actiontask_counts, sender=ActionTask)
models.signals.post_save.connect(user_post_save, sender=User)
models.signals.post_save.connect(update_commited_action, sender=UserActionProgress)