import datetime
import inspect
import random
import re

from django import template
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db import models

from utils import hash_val

URL_REGEX = re.compile(r"\b(https?)://[-A-Z0-9+&@#/%?=~_|!:,.;]*[-A-Z0-9+&@#/%=~_|]", re.IGNORECASE)

class Message(models.Model):
    TIMING_TYPES = (
        ("after_start", "Send X hours after start",),
        ("before_end", "Send X hours before end",),
        ("after_end", "Send X hours after end",),
        ("timeline_scale", "Send at X percent complete"),
    )
    TIMING_CODES = [t[0] for t in TIMING_TYPES]
    
    name = models.CharField(max_length=50, unique=True, db_index=True)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sends = models.PositiveIntegerField(default=0)
    message_timing = models.CharField(max_length=20, choices=TIMING_TYPES, help_text="This option\
        is directly related to x_value. To determine the send time of a message, use this\
        field to select HOW a send time is calculated. Then use x_value to determine the\
        variable X in message timing. For example: if we choose 'Send X hours after start' and a\
        x_value of 48. The message will be sent out 48 hours after the start. So in the\
        case of a commitment stream, 48 hours after they make a commitment.")
    x_value = models.PositiveIntegerField()
    recipient_function = models.CharField(max_length=100, help_text="This is an attribute or function\
        of the content object that defines a recipient or list of recipeients.  Note: recipients\
        can be classified as email addresses or objects that contain an 'email' attribute (e.g.\
        auth.User or events.Guest)")
    send_as_batch = models.BooleanField(default=False, help_text="If multiple messages of the\
        same type are scheduled to be sent out at the same time, then just send one. Note: if you\
        check this box, your messages must be written to reference multiple objects.  Be very\
        careful when using this option in conjunction with AB Tests.")
    # batch_function = models.CharField(max_length=100, help_text="This is an attribute or function\
    #     of the content object that defines a value all like messages should match on. If this field\
    #     is not defined, then the messages will match on the content object itself.")
    batch_window = models.PositiveIntegerField(null=True, blank=True, help_text="Only applicable if a\
        message is scheduled to be sent as a batch, but if set, all messages of this type will\
        be batched together if their send time is calculated to be within X hours of one another.")
    time_snap = models.TimeField(null=True, blank=True, help_text="Use this option to ensure a message\
        is sent out at a particular time of day.  Once the send time is calculated, time_snap\
        will reset the time value leaving the date intact. For example if the send time is\
        calculated to July 15th, 2010 at 3:32pm and time_snap is set to 11:00am. The new send\
        time will be July 15th, 2010 at 11:00am.")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def send_time(self, start, end):
        """
        Note that if an 'after start' or 'before end' send time is created, and it falls
        outside of the start, end range.  This function will return None, meaning the message
        should not be sent
        """
        if self.message_timing not in Message.TIMING_CODES:
            raise NotImplementedError("unknown delta type: %s" % self.message_timing)
            
        if start.__class__ == datetime.date:
            start = datetime.datetime.combine(start, datetime.time.min)
        if end.__class__ == datetime.date:
            end = datetime.datetime.combine(end, datetime.time.max)
        if self.message_timing == "timeline_scale":
            timeline = end - start
            delta = (timeline * self.x_value) / 100
            send_time = start + delta
        else:
            delta = datetime.timedelta(hours=self.x_value)
            if self.message_timing == "after_start":
                send = start + delta
                send_time = send if send < end else None
            elif self.message_timing == "before_end":
                send = end - delta
                send_time = send if send > start else None
            elif self.message_timing == "after_end":
                send_time = end + delta
        if self.time_snap:
            return send_time.replace(hour=self.time_snap.hour, minute=self.time_snap.minute, 
                second=self.time_snap.second)
        return send_time
    
    def recipients(self, content_object):
        """
        The function that is invoked to gather the recipients can return one of four things.
            1. email address
            2. object (with attribute 'email')
            3. list of email addresses
            4. list of objects (such that each object as the 'email' attribute)
        
        Regardless of what the invoked function returns, this function is responsible for returning
        a 2-tuple, where the first value is the email address and the second value is the object.
        If the object isn't defined this will be set to None.
        """
        if not hasattr(content_object, self.recipient_function):
            raise NotImplementedError("%s does not exist for %s" % (self.recipient_function,
                content_object))
        func_or_attr = getattr(content_object, self.recipient_function)
        recipients = func_or_attr() if inspect.ismethod(func_or_attr) else func_or_attr
        if not hasattr(recipients, "__iter__"):
            recipients = [recipients]
        return [(r.email, r) if hasattr(r, "email") else (r, None) for r in recipients]
        
    # def batch_type(self, content_object):
    #     if not hasattr(content_object, self.batch_function):
    #         raise NotImplementedError("%s does not exist for %s" % (self.batch_function,
    #             content_object))
    #     func_or_attr = getattr(content_object, self.batch_function)
    #     return func_or_attr() if inspect.ismethod(func_or_attr) else func_or_attr
    
    def send(self, content_object, blacklisted_emails=None): # TODO: create unit tests for Message.send()
        sent = []
        if not blacklisted_emails:
            blacklisted_emails = []
        for email, user_object in self.recipients(content_object):
            if email in blacklisted_emails:
                continue # email has been blacklisted, don't send to this recipient
            # for each recipient, create a Recipient message to keep track of opens
            recipient_message = RecipientMessage.objects.create(message=self, recipient=email,
                token=hash_val([email, datetime.datetime.now()]))
            domain = Site.objects.get_current().domain
            context = template.Context({"content_object": content_object, "domain": domain,
                "recipient": user_object if user_object else email })
            # render the body template with the given, template
            body = template.Template(self.body).render(context)
            for index, link in enumerate([m.group() for m in URL_REGEX.finditer(body)]):
                # for each unique link in the body, create a Message link to track the clicks
                ml = MessageLink.objects.create(recipient_message=recipient_message,
                    link=link, token=hash_val([index, datetime.datetime.now()]))
                tracker = "http://%s%s" % (domain, reverse("message_click", args=[ml.token]))
                # replace the original link with traking URL
                body = body.replace(link, tracker, 1)
            open_link = '<img src="http://%s%s"></img>' % (domain, reverse("message_open", args=[recipient_message.token]))
            # insert an open tracking image into the body
            body += open_link
            msg = EmailMessage(self.subject, body, None, [email])
            msg.content_subtype = "html"
            msg.send()
            self.sends += 1 # after the message is sent, increment the sends count
            self.save()
            sent.append(Sent.objects.create(message=self, recipient=email, email=msg.message()))
        return sent
    
    def unique_opens(self):
        opens = RecipientMessage.objects.filter(message=self, opens__gt=0).aggregate(
            models.Count("opens"))["opens__count"]
        return opens if opens else 0
        
    def related_streams(self):
        return Stream.objects.filter(models.Q(abtest__message=self) | models.Q(abtest__test_message=self))
        
    def blacklisted_emails(self):
        """
        For a given message, collect all of the streams this message is related to, then
        build a list of all emails (derieved from users) that have indicated they do not wish
        to recieve emails.
        """
        blacklisted_emails = []
        for stream in self.related_streams():
            blacklisted_emails = blacklisted_emails + stream.blacklisted_emails()
        return blacklisted_emails
    
    def __unicode__(self):
        return self.name

class RecipientMessage(models.Model):
    message = models.ForeignKey(Message)
    recipient = models.EmailField()
    token = models.CharField(max_length=40, editable=False, unique=True, db_index=True)
    opens = models.PositiveIntegerField(default=0, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class MessageLink(models.Model):
    recipient_message = models.ForeignKey(RecipientMessage)
    link = models.URLField(verify_exists=False)
    token = models.CharField(max_length=40, editable=False, unique=True, db_index=True)
    clicks = models.PositiveIntegerField(default=0, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class QueueManager(models.Manager):
    def send_ready_messages(self, process_minutes=12):
        now = datetime.datetime.now()
        if process_minutes:
            until = now + datetime.timedelta(minutes=process_minutes)
        sent = []
        deleted_pk = []
        for queued_message in self.filter(send_time__lte=now).order_by("send_time"):
            if queued_message.pk in deleted_pk:
                continue # previous batchable message has been sent, and this one has now been deleted
            batchable_messages = queued_message.find_batchable_messages()
            if batchable_messages:
                # TODO: should regenerate message, will need to make ABTest/Message One To One first
                deleted_pk = deleted_pk + [bm.pk for bm in batchable_messages]
                batchable_messages.delete()
            sent = sent + queued_message.send()
            queued_message.delete()
            if process_minutes and until < datetime.datetime.now():
                print "WARNING: %s min time limit has been exceeded" % process_minutes
                break
        return sent

class Queue(models.Model):
    message = models.ForeignKey(Message)
    content_type = models.ForeignKey(ContentType, verbose_name="content type", related_name="%(class)s")
    object_pk = models.PositiveIntegerField("object ID")
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    batch_content_type = models.ForeignKey(ContentType, verbose_name="batch content type", 
        related_name="%(class)s_batch", null=True)
    batch_object_pk = models.PositiveIntegerField("batch object ID", null=True)
    batch_content_object = generic.GenericForeignKey(ct_field="batch_content_type", fk_field="batch_object_pk")
    send_time = models.DateTimeField(db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = QueueManager()
    
    def send(self):
        return self.message.send(content_object=self.content_object, 
            blacklisted_emails=self.message.blacklisted_emails())
    
    def find_batchable_messages(self):
        if not self.message.send_as_batch:
            return None
        potential_messages = ABTest.objects.potential_messages(message=self.message)
        delta_time = datetime.timedelta(hours=self.message.batch_window) if self.message.batch_window else datetime.timedelta(0)
        queued = Queue.objects.filter(message__in=potential_messages, batch_content_type=self.batch_content_type,
            batch_object_pk=self.batch_object_pk, send_time__lte=self.send_time+delta_time).exclude(pk=self.pk)
        return queued if queued else None
            
    def __unicode__(self):
        return "%s" % (self.pk)
        
class StreamManager(models.Manager):
    def streams_not_blacklisted_by_user(self, user):
        return self.exclude(pk__in=user.blacklisted_set.all())

class Stream(models.Model):
    slug = models.SlugField(db_index=True, unique=True)
    label = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    can_unsubscribe = models.BooleanField(default=True)
    blacklisted = models.ManyToManyField("auth.User", through="StreamBlacklist", 
        related_name="blacklisted_set")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = StreamManager()
    
    def _queued_messages(self, content_object):
        potential_messages = ABTest.objects.potential_messages(stream=self)
        return Queue.objects.filter(message__in=potential_messages, object_pk=content_object.pk,
            content_type=ContentType.objects.get_for_model(content_object))
    
    def enqueue(self, content_object, start, end, batch_content_object=None, send_expired=True):
        enqueued = []
        now = datetime.datetime.now()
        for ab_test in ABTest.objects.filter(stream=self):
            if not ab_test.is_enabled:
                continue
            message = ab_test.random_message()
            send_time = message.send_time(start, end)
            if send_time:
                if send_time <= now:
                    if send_expired:
                        message.send(content_object)
                else:
                    if batch_content_object:
                        enqueued.append(Queue.objects.create(message=message,
                            content_object=content_object, send_time=send_time, 
                            batch_content_object=batch_content_object))
                    else:
                        enqueued.append(Queue.objects.create(message=message,
                            content_object=content_object, send_time=send_time))
        return enqueued
    
    def upqueue(self, content_object, start, end, batch_content_object=None):
        self.dequeue(content_object=content_object)
        return self.enqueue(content_object=content_object, start=start, end=end, 
            batch_content_object=batch_content_object, send_expired=False)
    
    def dequeue(self, content_object):
        return self._queued_messages(content_object).delete()
        
    def blacklisted_emails(self):
        return [u.email for u in self.blacklisted.all()]
    
    def __unicode__(self):
        return self.label
        
class ABTestManager(models.Manager):
    def potential_messages(self, message=None, stream=None):
        query = self
        if message:
            query = query.filter(models.Q(message=message) | models.Q(test_message=message))
        if stream:
            query = query.filter(stream=stream)
        potential_messages = []
        for ab_test in query:
            potential_messages.append(ab_test.message)
            potential_messages.append(ab_test.test_message)
        return list(set(potential_messages))

class ABTest(models.Model):
    message = models.ForeignKey(Message, related_name="message")
    test_message = models.ForeignKey(Message, related_name="test_message", null=True, blank=True)
    test_percentage = models.PositiveIntegerField(default=0)
    is_enabled = models.BooleanField(default=True)
    stream = models.ForeignKey(Stream)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ABTestManager()
    
    def random_message(self):
        if not self.test_message or random.randint(0, 100) > self.test_percentage:
            return self.message
        else:
            return self.test_message
    
    def control_sends(self):
        return self.message.sends
    
    def control_opens(self):
        return self.message.unique_opens()
    
    def test_sends(self):
        return self.test_message.sends
    
    def test_opens(self):
        return self.test_message.unique_opens()
    
    def __unicode__(self):
        return "%s [test: %s @ %s%%]" % (self.message, self.test_message, self.test_percentage)

class Sent(models.Model):
    message = models.ForeignKey(Message)
    recipient = models.CharField(max_length=100)
    email = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s" % self.message
        
class StreamBlacklist(models.Model):
    """
    Any user listed in this table will not recieve emails for the stream they are linked to.
    """
    user = models.ForeignKey("auth.User")
    stream = models.ForeignKey(Stream)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "stream",)

    def __unicode__(self):
        return u"%s will not recieve emails for %s streams" % (self.user, self.stream)