from django.db import models
from utils import profileit, progressBar

class DefaultModel(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.name
        
class GroupManager(models.Manager):
    def create_test_group(self, number):
        """create 1 group with x random users"""
        import random
        id = self.all().aggregate(models.Max("id"))["id__max"]
        next_id = id + 1 if id else 1
        name = "group_%s_%s" % (number, next_id)
        group = Group(name=name)
        group.save()
        user_id_list = [user["id"] for user in User.objects.all().values("id")]
        for i in range(number):
            user_id = user_id_list.pop(random.randint(0, len(user_id_list)-1))
            group.user_set.add(User.objects.get(id=user_id))
        return group
        
class Group(DefaultModel):
    objects = GroupManager()
    
    def how_many_members(self):
        return self.user_set.all().count()
      
    def completed_actions_by_user(self):
        """
        what actions have been completed by users in this group and how many users have completed each action
        """
        actions = Action.objects.filter(actiontask__record__user__groups=self).extra(select={'user_id': 'demo_user.id'}).annotate(user_completes=models.Count("actiontask__record__user"))        
        completed = dict([(action, []) for action in actions if action.total_tasks == action.user_completes])
        [completed[action].append(action.user_id) for action in actions if action.total_tasks == action.user_completes]
        
        return completed
        
    def completed_actions_by_user_denorm(self):
        """
        what actions have been completed by users in this group and how many users have completed each action
        """
        return list(Action.objects.filter(useractionprogress__user__groups=self, useractionprogress__completes=models.F("total_tasks")))
        
    def members_with_points(self):
        return list(User.objects.filter(groups=self).annotate(total_points=models.Sum("record__points")))
        
    def get_latest_records(self, quantity=None):
        records = Record.objects.filter(user__groups=self)
        return records[:quantity] if quantity else list(records)
        
class UserManager(models.Manager):
    def create_test_users(self, number):
        """create x number of users with incremental names"""
        id = self.all().aggregate(models.Max("id"))["id__max"]
        next_id = id + 1 if id else 1
        user_ids = []
        for id in range(number):
            name = "user_%s" % (id+next_id)
            user = User(name=name)
            user.save()
            user_ids.append(user.id)
        return user_ids
        
class User(DefaultModel):
    groups = models.ManyToManyField(Group)
    objects = UserManager()
    
    def get_latest_records(self, quantity=None):
        records = self.record_set.all()
        return records[:quantity] if quantity else records
        
    def get_total_points(self):
        return self.record_set.all().aggregate(models.Sum("points"))["points__sum"]
        
    def record_activity(self, activity):
        return Record(user=self, activity=activity, points=activity.points).save()
        
    def unrecord_activity(self, activity):
        Record.objects.filter(user=self, activity=activity).delete()
     
    def actions_with_additions(self):
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
        actions = Action.objects.select_related().all().annotate(total_tasks=models.Count("actiontask")).annotate(total_points=models.Sum("actiontask__points"))
        action_tasks = ActionTask.objects.all().extra(
            select_params = (self.id,), 
            select = { 'completed': 'SELECT demo_record.created \
                                     FROM demo_record \
                                     WHERE demo_record.user_id = %s AND \
                                     demo_record.activity_id = demo_activity.id' })
                                     
        actiontask_dict = dict([(at.id, at) for at in action_tasks])
        print actiontask_dict
        for action in actions:
            total_completes = 0
            for actiontask in action.actiontask_set.all():
                actiontask.completed = actiontask_dict[actiontask.id].completed
                total_completes += 1 if actiontask.completed else 0
            action.total_completes = total_completes
            
        not_complete = [action for action in actions if action.total_completes == 0]
        in_progress = [action for action in actions if action.total_tasks > action.total_completes and action.total_completes > 0]
        completed = [action for action in actions if action.total_tasks == action.total_completes]

        return (actions, not_complete, in_progress, completed)
        
    def get_chart_data(self):
        records = self.get_latest_records().select_related().order_by("created")
        
        dates = dict([(record.created.date, ChartPoint(record.created.date)) for record in records]) #create a new dict of dates to ChartPoints
        [dates[record.created.date].add_record(record) for record in records] #for each record add it to its cooresponding ChartPoint
        
        return dates
    
class Action(DefaultModel):
    total_tasks = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    users_in_progress = models.IntegerField(default=0)
    users_completed = models.IntegerField(default=0)
    user_progress = models.ManyToManyField(User, through="UserActionProgress")
    
    def users_with_completes(self):
        """
        return a 3-tuple query set of user object lists, such that each user object has an additional attribute, completes,
        which identifies how many tasks the user has completed for the given action.

        Note: only users that have began completeing task for the action will be listed

        The first list in the tuple is for all users that have made progress on the action, the second list is for all users
        that are working on the action (in progress) and the final list is for all users that have completed the action
        """
        total_tasks = self.actiontask_set.all().count()
        users = User.objects.filter(record__activity__actiontask__action=self).annotate(completes=models.Count("record"))
        in_progress = [user for user in users if total_tasks > user.completes and user.completes > 0]
        completed = [user for user in users if total_tasks == user.completes]

        return (users, in_progress, completed)
        
    def users_with_completes_denorm(self):
        in_progress_count = UserActionProgress.objects.filter(action=self, completed=0).count()
        completed_count = UserActionProgress.objects.filter(action=self, completed=1).count()

        in_progress = UserActionProgress.objects.select_related().filter(action=self, completed=0)[:5]
        completed = UserActionProgress.objects.select_related().filter(action=self, completed=1)[:5]

        return (in_progress_count, [uap.user for uap in in_progress], completed_count, [uap.user for uap in completed])
        
    def users_with_completes_denorm_raw(self):
        from django.db import connection, transaction
        cursor = connection.cursor()

        count_query = "SELECT COUNT(CASE WHEN completed = 0 THEN 1 END), COUNT(CASE WHEN completed = 1 THEN 1 END) FROM demo_useractionprogress WHERE action_id = %s" % self.id

        cursor.execute(count_query)
        in_progress_count, completed_count = cursor.fetchone()

        in_progress_where = "WHERE duap.action_id = %s AND duap.completed = 0" % self.id
        completed_where = "WHERE duap.action_id = %s AND duap.completed = 1" % self.id
        in_progress = list(User.objects.raw("SELECT * FROM demo_user du JOIN demo_useractionprogress duap ON du.id = duap.user_id %s LIMIT 5" % (in_progress_where)))
        completed = list(User.objects.raw("SELECT * FROM demo_user du JOIN demo_useractionprogress duap ON du.id = duap.user_id %s  LIMIT 5" % (completed_where)))

        return (in_progress_count, in_progress, completed_count, completed)
        
    def users_with_completes_denorm_best(self):
        in_progress = UserActionProgress.objects.select_related().filter(action=self, completed=0)[:5]
        completed = UserActionProgress.objects.select_related().filter(action=self, completed=1)[:5]

        return (self.users_in_progress, [uap.user for uap in in_progress], self.users_completed, [uap.user for uap in completed])
    
class Activity(DefaultModel):
    points = models.IntegerField(blank=True, null=True)
    users = models.ManyToManyField(User, through="Record")
    
class ActionTask(Activity):
    action = models.ForeignKey(Action)
    
class RecordManager(models.Manager):
    def create_random_records(self, mean, sigma=3.5, users=None):
        import math, random
        users = users if users != None else [user["id"] for user in User.objects.all().values("id")]
        activities = Activity.objects.all()
        activities_list = [act.id for act in activities]
        activities_dict = dict([(act.id, act) for act in activities])
        activities_len = len(activities_list)
        prog = progressBar(0, len(users), 50)
        oldprog = str(prog)
        for idx, user_id in enumerate(users):
            prog.updateAmount(idx)
            if oldprog != str(prog):
                print prog
                oldprog = str(prog)
            acopy = list(activities_list)
            records_to_create = int((random.gauss(mean, sigma) / 100) * activities_len)
            for i in range(records_to_create):
                activity_id = acopy.pop(random.randint(0, len(acopy)-1))
                Record(user_id=user_id, activity_id=activity_id, points=activities_dict[activity_id].points).save()
        print

class Record(models.Model):
    user = models.ForeignKey(User)
    activity = models.ForeignKey(Activity)
    points = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = RecordManager()
    
    class Meta:
        ordering = ["user", "activity", "created"]
    
    def __unicode__(self):
        return "%s records %s at %s" % (self.user, self.activity, self.created)
        
    # def __cmp__(self, other):
    #     if self.user != other.user:
    #         return cmp(self.user, other.user)
    #     try:
    #         action = self.activity.actiontask.action
    #     except Exception:
    #         action = None
    #     try:
    #         oaction = other.activity.actiontask.action
    #     except Exception:
    #         oaction = None
    #     return cmp(action, oaction) if action != oaction else cmp(self.created, other.created)
    
class UserActionProgress(models.Model):
        user = models.ForeignKey(User)
        action = models.ForeignKey(Action)
        completes = models.IntegerField(default=0)
        completed = models.IntegerField(default=0)
        
class ChartPoint(object):
    """docstring for ChartPoint"""
    def __init__(self, date):
        super(ChartPoint, self).__init__()
        self.date = date
        self.points = 0
        self.records = []
        
    def add_record(self, record):
        self.points += record.points
        self.records.append(record)

def actiontask_added(sender, **kwargs):
    actiontask_table_changed(sender, increase=True, **kwargs)
    
def actiontask_removed(sender, **kwargs):
    actiontask_table_changed(sender, increase=False, **kwargs)

def actiontask_table_changed(sender, instance, increase, **kwargs):
    print "instance is: %s" % instance.id
    if instance.id:
        instance.action.total_tasks += 1 if increase else -1
        instance.action.total_points += instance.points if increase else (-1 * instance.points)
        instance.action.save()
    
models.signals.post_save.connect(actiontask_added, sender=ActionTask)
models.signals.pre_delete.connect(actiontask_removed, sender=ActionTask)

def record_added(sender, **kwargs):
    record_table_changed(sender, increase=True, **kwargs)
    
def record_removed(sender, **kwargs):
    record_table_changed(sender, increase=False, **kwargs)

def record_table_changed(sender, instance, increase, **kwargs):
    # TODO: this entire function needs to be wrapped in a transaction
    try:
        action = instance.activity.actiontask.action
        obj, created = UserActionProgress.objects.get_or_create(user=instance.user, action=action)
        new_completes = obj.completes + 1 if increase else  obj.completes - 1
        new_completed = 1 if new_completes >= action.total_tasks else 0
        inprogress = 1  if obj.completed != 1 and obj.completes > 0 else 0 # the useraction is currently in_progress if it is not completed, but the completes count is greater than 0
        new_inprogress = 1 if new_completed != 1 and new_completes > 0 else 0 # the useraction is going to be in_progress if it will not be completed, but the new completes count is greater than 0
        
        if obj.completed != new_completed:
            action.users_completed += new_completed - obj.completed
        if inprogress != new_inprogress:
            action.users_in_progress += new_inprogress - inprogress
        if obj.completed != new_completed or inprogress != new_inprogress:
            action.save()
        
        obj.completes = new_completes
        obj.completed = new_completed
        obj.save()
    except ActionTask.DoesNotExist:
        pass
        
models.signals.post_save.connect(record_added, sender=Record)
models.signals.pre_delete.connect(record_removed, sender=Record)