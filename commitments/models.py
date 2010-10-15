import datetime

from django.db import models
from django.contrib.auth.models import User

from geo.models import Location

class Contributor(models.Model):
    first_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(blank=True, max_length=50)
    email = models.EmailField(blank=True, null=True, db_index=True)
    phone = models.CharField(blank=True, max_length=12)
    location = models.ForeignKey("geo.Location", blank=True, null=True)
    user = models.ForeignKey("auth.User", blank=True, null=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = (("user",),("email",),)
        ordering = ['first_name', 'last_name']
        permissions = (("edit_any_contributor", "Can edit any contributor"),)
        
    def __init__(self, *args, **kwargs):
        super(Contributor, self).__init__(*args, **kwargs)
        self.contributor_profile = ContributorProfile(self)
        
    def _set_name(self, value):
        first, space, last = value.partition(" ")
        self.first_name = first
        self.last_name = last
    def _get_name(self):
        if self.user:
            return self.user.get_full_name()
        return ("%s %s" % (self.first_name, self.last_name)).strip()
    name = property(_get_name, _set_name)
    
    def _set_zipcode(self, value):
        try:
            self.location = Location.objects.get(zipcode=value)
        except Location.DoesNotExist:
            self.location = None
    def _get_zipcode(self):
        return self.location.zipcode if self.location else ""
    zipcode = property(_get_zipcode, _set_zipcode)
    
    def needs_more_info(self):
        return not (self.user or (self.first_name and self.email))
        
    def has_made_commitments(self):
        return Commitment.objects.filter(contributor=self).exists()
        
    def get_profile(self):
        # Note: this is somewhat of a hack to get Commitment objects to behave like UserActionProgress objects
        return self.contributor_profile
    get_profile = property(get_profile)
    
    def get_full_name(self):
        if self.user:
            return self.user.get_full_name()
        elif self.name:
            return self.name
        else:
            return self.email
            
    def __unicode__(self):
        return self.get_full_name()
        
class ContributorProfile(object):
    def __init__(self, contributor):
        self.contributor = contributor

    def potential_points(self):
        return Commitment.objects.pending_commitments(contributor=self.contributor).aggregate(
            models.Sum("action__points"))["action__points__sum"]

    def number_of_committed_actions(self):
        return Commitment.object.pending_commitments(contributor=self.contributor).count()

    def commitments_made_yestarday(self):
        start = datetime.datetime.combine(yestarday(), datetime.time.min)
        end = datetime.datetime.combine(yestarday(), datetime.time.max)
        return Commitment.objects.pending_commitments(contributor=self.contributor).filter(
            updated__gte=start, updated__lte=end)

    def commitments_made_before_yestarday(self):
        start = datetime.datetime.combine(yestarday(), datetime.time.min)
        return Commitment.objects.pending_commitments(contributor=self.contributor).filter(
            updated__lt=start)

    def commitments_made_last_24_hours(self):
        return Commitment.objects.pending_commitments(contributor=self.contributor).filter(
            updated__gte=yestarday())

    def commitments_made_more_than_24_hours(self):
        return Commitment.objects.pending_commitments(contributor=self.contributor).filter(
            updated__lt=yestarday())

    def commitments_due_in_a_week(self):
        return self._commitment_due_on(datetime.date.today() + datetime.timedelta(days=7))

    def commitments_due_today(self):
        return self._commitment_due_on(datetime.date.today())

    def _commitment_due_on(self, due_date):
        commitments = Commitment.objects.pending_commitments(contributor=self.contributor)
        return [c for c in commitments if c.date_committed == due_date]
        
class SurveyManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)
    
class Survey(models.Model):
    name = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=50)
    form_name = models.CharField(max_length=75)
    template_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    contributors = models.ManyToManyField(Contributor, through="ContributorSurvey")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = SurveyManager()
    
    class Meta:
        ordering = ['name', 'updated']
        
    def __unicode__(self):
        return "%s Survey" % self.name
        
    def natural_key(self):
        return [self.name]
        
    def questions(self):
        import survey_forms
        form = getattr(survey_forms, self.form_name)(None, None)
        return form.fields.keys()
        
class ContributorSurvey(models.Model):
    contributor = models.ForeignKey(Contributor)
    survey = models.ForeignKey(Survey)
    entered_by = models.ForeignKey("auth.user")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
        
    class Meta:
        unique_together = (("contributor", "survey", "entered_by",),)
        
class CommitmentManager(models.Manager):
    def pending_commitments(self, contributor=None):
        queryset = self.filter(answer="C", action__isnull=False)
        return queryset if not contributor else queryset.filter(contributor=contributor)
        
class Commitment(models.Model):
    contributor = models.ForeignKey(Contributor, db_index=True)
    question = models.CharField(max_length=50)
    answer = models.CharField(max_length=100)
    action = models.ForeignKey("actions.Action", null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = CommitmentManager()

    class Meta:
        unique_together = (("contributor", "question",),)
        
    def _get_user(self):
        # Note: this is somewhat of a hack to get Commitment objects to behave like UserActionProgress objects
        return self.contributor
    user = property(_get_user)
    
    def _get_date_committed(self):
        # Note: this is somewhat of a hack to get Commitment objects to behave like UserActionProgress objects
        if self.action and self.answer == "C":
            return (self.updated + datetime.timedelta(weeks=3)).date()
        return None
    date_committed = property(_get_date_committed)
    
def link_contributor_to_user(sender, instance, **kwargs):
    if instance.email:
        try:
            user = User.objects.get(email=instance.email)
            instance.user = user
        except User.DoesNotExist:
            instance.user = None
models.signals.pre_save.connect(link_contributor_to_user, sender=Contributor)
    
def link_new_user_to_contributor(sender, instance, created, **kwargs):
    """
    When a user registers, see if they exists as a contributor record and if so, link them up.
    """
    if created and instance.email:
        try:
            contributor = Contributor.objects.get(email=instance.email)
            contributor.user = instance
            contributor.save()
        except Contributor.DoesNotExist:
            pass
models.signals.post_save.connect(link_new_user_to_contributor, sender=User)