import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

import tagging

from records.models import Record
from dated_static.templatetags.dated_static import dated_static

class ActionManager(models.Manager):
    
    def get_popular(self, count=5):
        # Returns the most popular actions where popularity is defined as the sum of completed and commited users
        # TODO: Write a unit test for get_popular
        actions = Action.objects.all()
        count = actions.count() if actions.count() < count else count
        return sorted(actions, reverse=True, key=lambda action: action.users_completed+action.users_committed)[:count]
    
    def actions_by_status(self, user):
        actions = Action.objects.select_related().all().extra(select_params = (user.id,), 
                    select = { 'completed': 'SELECT uap.is_completed FROM actions_useractionprogress uap \
                                             WHERE uap.user_id = %s AND uap.action_id = actions_action.id'
                    }).extra(select_params = (user.id,),
                    select = { 'committed': 'SELECT uap.date_committed FROM actions_useractionprogress uap \
                                             WHERE uap.user_id = %s AND uap.action_id = actions_action.id'
                    })
        actions = sorted(actions, key=lambda a: not a.has_illustration())
        recommended = [a for a in actions if a.completed != 1 and a.committed == None]
        committed = [a for a in actions if a.completed != 1 and a.committed != None]
        completed = [a for a in actions if a.completed == 1]
        return actions, recommended, committed, completed
        
class Action(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    teaser = models.TextField()
    content = models.TextField()
    points = models.IntegerField(default=0)
    users_completed = models.IntegerField(default=0)
    users_committed = models.IntegerField(default=0)
    users = models.ManyToManyField(User, through="UserActionProgress")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ActionManager()
    
    def complete_for_user(self, user):
        uap, created = UserActionProgress.objects.get_or_create(user=user, action=self)
        was_completed = uap.is_completed
        uap.is_completed = True
        uap.save()
        if not was_completed:
            Record.objects.create_record(user, "action_complete", self)
            
    def undo_for_user(self, user):
        try:
            uap = UserActionProgress.objects.get(user=user, action=self)
            was_completed = uap.is_completed
            uap.is_completed = False
            uap.save()
            if was_completed:
                Record.objects.void_record(user, "action_complete", self)
        except UserActionProgress.DoesNotExist:
            return False
        return True
            
    def commit_for_user(self, user, date):
        uap, c = UserActionProgress.objects.get_or_create(user=user, action=self)
        was_committed = uap.date_committed <> None
        uap.date_committed = date
        uap.save()
        if not was_committed:
            Record.objects.create_record(user, "action_commitment", self, data={"date_committed": date})
            
    def cancel_for_user(self, user):
        try:
            uap = UserActionProgress.objects.get(user=user, action=self)
            was_committed = uap.date_committed <> None
            uap.date_committed = None
            uap.save()
            if was_committed:
                Record.objects.void_record(user, "action_commitment", self)
        except UserActionProgress.DoesNotExist:
            return False
        return True
        
    def tag_list(self):
        tag_names = [t.name for t in self.tags]
        return ", ".join(tag_names) if tag_names else ""
    tag_list.short_description = "Tags"
    
    def action_forms_with_data(self, user):
        return ActionForm.objects.filter(action=self).extra(
                select_params = (user.id,),
                select = { "data": """SELECT afd.data
                                        FROM actions_actionformdata afd
                                        WHERE afd.user_id = %s
                                        AND actions_actionform.id = afd.action_form_id"""})
                                        
    def get_detail_illustration(self):
        return dated_static("images/actions/%s/action_detail.jpg" % self.slug)

    def get_nugget_illustration(self):
        return dated_static("images/actions/%s/action_nugget.jpg" % self.slug)
    
    def has_illustration(self):
        path = "images/actions/%s/action_detail.jpg" % self.slug
        return os.path.exists(os.path.join(settings.MEDIA_ROOT, path))
    
    def __unicode__(self):
        return u"%s" % self.name

    @models.permalink
    def get_absolute_url(self):
        return ("action_detail", [str(self.slug)])
tagging.register(Action)

class UserActionProgressManager(models.Manager):
    def commitments_for_user(self, user):
         return self.select_related().filter(user=user, is_completed=False, date_committed__isnull=False).order_by("date_committed")

class UserActionProgress(models.Model):
    user = models.ForeignKey(User)
    action = models.ForeignKey(Action)
    is_completed = models.BooleanField(default=False)
    date_committed = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = UserActionProgressManager()
    
    class Meta:
        unique_together = ("user", "action",)
    
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
    var_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("action", "form_name",)
    
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
    data = models.TextField()
    # TODO: make ActionFormData.data a serialized field
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("action_form", "user",)
    
    def __unicode__(self):
        return u"%s is working on %s" (self.user, self.action_form)

"""
SIGNALS!
"""
def update_action_aggregates(sender, instance, **kwargs):
    instance.action.users_completed = UserActionProgress.objects.filter(action=instance.action, is_completed=True).count()
    instance.action.users_committed = UserActionProgress.objects.filter(action=instance.action, date_committed__isnull=False).count()
    instance.action.save()

models.signals.post_save.connect(update_action_aggregates, sender=UserActionProgress)