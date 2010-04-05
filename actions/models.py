from django.db import models
from django.contrib.auth.models import User

import tagging

class ActionManager(models.Manager):
    def actions_by_status(self, user):
        actions = Action.objects.select_related().all().extra(select_params = (user.id,), 
                    select = { 'completed': 'SELECT uap.is_completed FROM actions_useractionprogress uap \
                                             WHERE uap.user_id = %s AND uap.action_id = actions_action.id'
                    }).extra(select_params = (user.id,),
                    select = { 'committed': 'SELECT uap.date_committed FROM actions_useractionprogress uap \
                                             WHERE uap.user_id = %s AND uap.action_id = actions_action.id'
                    })
        recommended = [a for a in actions if a.completed != 1 and a.committed == None]
        committed = [a for a in actions if a.completed != 1 and a.committed != None]
        completed = [a for a in actions if a.completed == 1]
        return actions, recommended, committed, completed

class Action(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    teaser = models.TextField()
    content = models.TextField()
    points = models.IntegerField(default=0)
    users_completed = models.IntegerField(default=0)
    users_committed = models.IntegerField(default=0)
    users = models.ManyToManyField(User, through="UserActionProgress")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ActionManager()

    def __unicode__(self):
        return u"%s" % self.name

    @models.permalink
    def get_absolute_url(self):
        return ("action_detail", [str(self.slug)])
tagging.register(Action)

class UserActionProgress(models.Model):
    user = models.ForeignKey(User)
    action = models.ForeignKey(Action)
    is_completed = models.IntegerField(default=0)
    date_committed = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u"%s is working on %s" % (self.user, self.action)
        
class ActionForm(models.Model):
    """
    ActionForm is used to link a worksheet form to an action.  Since we will use
    introspection to create an instance of the form, it is imparitive that the form_name
    field match the action class name of the django form.
    """
    action = models.ForeignKey(Action)
    form_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u"%s is using form %s" % (self.action, self.form_name)
        
class ActionFormData(models.Model):
    """
    ActionFormData is used to store a users state for a particular action form, the
    data field will contain serialized data that can be reformed into a request.POST
    dict and initialized with the corresponding ActionForm.
    """
    action_form = models.ForeignKey(ActionForm)
    user = models.ForeignKey(User)
    data = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u"%s is working on %s" (self.user, self.action_form)

"""
SIGNALS!
"""
def update_action_aggregates(sender, instance, **kwargs):
    instance.action.users_completed = UserActionProgress.objects.filter(action=instance.action, is_completed=1).count()
    instance.action.users_committed = UserActionProgress.objects.filter(action=instance.action, date_committed__isnull=False).count()
    instance.action.save()

models.signals.post_save.connect(update_action_aggregates, sender=UserActionProgress)