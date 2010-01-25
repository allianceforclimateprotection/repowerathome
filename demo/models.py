from django.db import models

class DefaultModel(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.name
        
class Group(DefaultModel):
    pass
        
class User(DefaultModel):
    groups = models.ManyToManyField(Group)
    
    def get_latest_records(self, quantity=None):
        records = self.record_set.all()
        return records[:quantity] if quantity else records
        
    def get_total_points(self):
        return self.record_set.all().aggregate(models.Sum("points"))["points__sum"]
        
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
        
    def record_activity(activity):
        Record(user=self, activity=activity, points=activity.points).save()
    
    def unrecord_activity(activity):
        Record.objects.filter(user=self, activity=activity).delete()
        
    def get_chart_data(self):
        tooltip_template = loader.get_template("rah/_chart_tooltip.html")
        records = self.get_latest_records().select_related().order_by("created")
        
        dates = dict([(action.created.date, ChartPoint(action.created.date, tooltip_template)) for record in records]) #create a new dict of dates to ChartPoints
        [dates[record.created.date].add_record(record) for record in records] #for each record add it to its cooresponding ChartPoint
        
        return json.dumps({ "point_data": [(date.date, date.points) for date in dates], "tooltips": [(date.render_tooltip()) for date in dates] })
    
class Action(DefaultModel):
    
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
    
class Activity(DefaultModel):
    points = models.IntegerField(blank=True, null=True)
    users = models.ManyToManyField(User, through="Record")
    
class ActionTask(Activity):
    action = models.ForeignKey(Action)
    
class Record(models.Model):
    user = models.ForeignKey(User)
    activity = models.ForeignKey(Activity)
    points = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "%s records %s at %s" % (self.user, self.activity, self.created)
        
class ChartPoint(object):
    """docstring for ChartPoint"""
    def __init__(self, date, tooltip_template):
        super(ChartPoint, self).__init__()
        self.date = date
        self.tooltip_template = tooltip_template
        self.points = 0
        self.records = []
        
    def add_record(self, record):
        self.points += record.points
        self.records.append(record)
        
    def render_tooltip(self):
        return self.tooltip_template.render(Context(self.records))
        