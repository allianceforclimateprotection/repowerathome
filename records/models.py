import base64, time
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template import Context, loader
from datetime import datetime, timedelta
from django.contrib.auth.models import User

try:
    import cPickle as pickle
except:
    import pickle

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

class RecordManager(models.Manager):
    def get_query_set(self):
        return super(RecordManager, self).get_query_set().filter(void=False)

    def user_records(self, user, quantity=None):
        records = user.record_set.all()
        return records[:quantity] if quantity else records

    def last_active(self, user):
        return Record.objects.filter(user=user).aggregate(la=models.Max("created"))["la"]

    def create_record(self, user, activity, content_object=None, data=None):
        """
        user: A user object (required)
        activity: str or Activty object (required) 
        content_object: A model object to associate with the record
        data: A python dictionary with additional data to be stored with the record 
        """
        if type(activity) is str:
            activity = Activity.objects.get(slug=activity)

        # Figure out how many points we're going to give.
        points = content_object.points if hasattr(content_object, "points") else activity.points

        # Add a new content_object (and don't create a new record) if this is batachable
        if activity.batch_time_minutes and content_object:
            # see if one exists in timeframe
            batch_minutes = activity.batch_time_minutes
            cutoff_time = datetime.now()-timedelta(minutes=batch_minutes)
            batchable_items = Record.objects.filter(user=user, activity=activity, 
                                                    created__gt=cutoff_time).order_by('-created').all()[0:1]

            if batchable_items:
                batchable_items[0].content_objects.create(content_object=content_object)
                batchable_items[0].is_batched = True
                batchable_items[0].points += points
                batchable_items[0].save()
                return batchable_items[0]

        record = Record.objects.create(user=user, activity=activity, data=data, points=points)
        if content_object: record.content_objects.create(content_object=content_object)
        record.save()
        return record

    def void_record(self, user, activity, content_object):
        if type(activity) is str:
            activity = Activity.objects.get(slug=activity)
        record = Record.objects.filter(user=user, activity=activity, content_objects__object_id=content_object.id)[0:1]
        if record:
            record[0].void = True
            record[0].save()
    
    def get_chart_data(self, user):
        records = self.user_records(user).select_related().order_by("created")
        chart_points = list(sorted(set([ChartPoint(record.created.date()) for record in records])))
        for chart_point in chart_points:
            [chart_point.add_record(record) for record in records if chart_point.date >= record.created.date()]

        return chart_points

class Activity(DefaultModel):
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
    objects = RecordManager()
    
    class Meta:
        ordering = ["-created"]
            
    def render(self):
        # TODO: Add a param to allow rendering specifically for the chart tooltip?
        if self.is_batched:
            template_file = "records/%s_batch.html" % self.activity.slug
        else:
            template_file = "records/%s.html" % self.activity.slug
        template = loader.get_template(template_file)
        content_object = self.content_objects.all()
        if content_object: content_object = content_object[0].content_object
        return template.render(Context({"record": self, "content_object":content_object}))

    def __unicode__(self):
        return "user: %s, activity: %s" % (self.user.get_full_name(), self.activity)

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
Signals!
"""
def update_profile_points(sender, instance, **kwargs):
    if instance.points == 0: return
    profile = instance.user.get_profile()
    total_points = Record.objects.filter(user=instance.user).aggregate(models.Sum('points'))['points__sum']
    profile.total_points = total_points if total_points else 0
    profile.save()
    
models.signals.post_save.connect(update_profile_points, sender=Record)