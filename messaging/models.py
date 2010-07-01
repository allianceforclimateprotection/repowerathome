import datetime
import random

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Message(models.Model):
    DELTA_TYPES = (
        ("after_start", "Send X hours after start",),
        ("before_end", "Send X hours before end",),
        ("after_end", "Send X hours after end",),
        ("timeline_scale", "Send at X percent complete"),
    )
    
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sends = models.PositiveIntegerField(default=0, editable=False)
    delta_type = models.CharField(max_length=20, choices=DELTA_TYPES)
    delta_value = models.PositiveIntegerField()
    recipient_function = models.CharField( max_length=100)
    
    def send_time(self, start, end):
        """
        Note that if an 'after start' or 'before end' send time is created, and it falls
        outside of the start, end range.  This function will return None
        """
        if self.delta_type == "timeline_scale":
            timeline = end - start
            delta = (timeline * self.delta_value) / 100
            return start + delta
        else:
            delta = datetime.timedelta(hours=self.delta_value)
            if self.delta_type == "after_start":
                send = start + delta
                return send if send < end else None
            elif self.delta_type == "before_end":
                send = end - delta
                return send if send > start else None
            elif self.delta_type == "after_end":
                return end + delta
        raise NotImplementedError("unknown delta type: %s" % self.delta_type)
        
    def recipients(self, content_object):
        if not hasattr(content_object, self.recipient_function):
            raise NotImplementedError("%s does not exist for %s" % (self.recipient_function, 
                content_object))
        return getattr(content_object, self.recipient_function)()
        
    def send(self):
        pass
        
    def __unicode__(self):
        return self.subject
        
class ABTest(models.Model):
    message = models.ForeignKey(Message, related_name="message")
    test_message = models.ForeignKey(Message, related_name="test_message")
    test_percentage = models.PositiveIntegerField()
    is_enabled = models.BooleanField(default=True)
    
    def random_message(self):
        if random.randint(0, 100) > self.test_percentage:
            return self.message
        else:
            return self.test_message
            
    def __unicode__(self):
        return "%s [test: %s]" % (self.message, self.test_message)
            
class RecipientMessage(models.Model):
    message = models.ForeignKey(Message)
    recipient = models.EmailField()
    token = models.CharField(max_length=30, editable=False)
    opens = models.PositiveIntegerField(default=0, editable=False)
    
class MessageLink(models.Model):
    recipient_message = models.ForeignKey(RecipientMessage)
    link = models.URLField(verify_exists=False)
    token = models.CharField(max_length=30, editable=False)
    clicks = models.PositiveIntegerField(default=0, editable=False)
    
class Queue(models.Model):
    message = models.ForeignKey(Message)
    content_type = models.ForeignKey(ContentType, verbose_name="content type", related_name="%(class)s")
    object_pk = models.PositiveIntegerField("object ID")
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    send_time = models.DateTimeField()
    
class StreamManager(models.Manager):
    def _queued_messages(slug, content_object):
        potential_messages = []
        for stream in self.filter(slug=slug):
            potential_messages.append(stream.ab_test.message)
            potential_messages.append(stream.ab_test.test_message)
        return Queue.objects.filter(message__in=potential_messages, object_pk=content_object.pk,
            content_type=ContentType.objects.get_for_model(content_object))
            
    def enqueue(slug, content_object, start, end):
        enqueued = []
        for stream in self.filter(slug=slug):
            message = stream.ab_test.message()
            send_time = message.send_time(start, end)
            if send_time:
                # TODO: if send_time is now, send instead of enqueue
                enqueued.append(Queue.objects.create(message=message, content_object=content_object, 
                    send_time=send_time))
        return enqueued
        
    def upqueue(slug, content_object, start, end):
        upqueued = self._queued_messages(slug, content_object)
        for message in upqueued:
            message.send_time = message.send_time(start, end)
            # TODO: if send_time is now or in the past, should we still send
            message.save()
        return upqueued
        
    def dequeue(slug, content_object):
        dequeued = self._queued_messages(slug, content_object)
        dequeued.delete()
        return dequeued
    
class Stream(models.Model):
    slug = models.SlugField(db_index=True)
    ab_test = models.ForeignKey(ABTest)
    objects = StreamManager()
    
    class Meta:
        unique_together = ("slug", "ab_test",)
    
