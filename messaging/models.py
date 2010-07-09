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

from utils import make_token

URL_REGEX = re.compile(r"\b(https?)://[-A-Z0-9+&@#/%?=~_|!:,.;]*[-A-Z0-9+&@#/%=~_|]", re.IGNORECASE)

class Message(models.Model):
    DELTA_TYPES = (
        ("after_start", "Send X hours after start",),
        ("before_end", "Send X hours before end",),
        ("after_end", "Send X hours after end",),
        ("timeline_scale", "Send at X percent complete"),
    )
    
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sends = models.PositiveIntegerField(default=0)
    delta_type = models.CharField(max_length=20, choices=DELTA_TYPES)
    delta_value = models.PositiveIntegerField()
    recipient_function = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def send_time(self, start, end):
        """
        Note that if an 'after start' or 'before end' send time is created, and it falls
        outside of the start, end range.  This function will return None, meaning the message
        should not be sent
        """
        if start.__class__ == datetime.date:
            start = datetime.datetime.combine(start, datetime.time.min)
        if end.__class__ == datetime.date:
            end = datetime.datetime.combine(end, datetime.time.max)
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
    
    def send(self, content_object):
        for email, user_object in self.recipients(content_object):
            # for each recipient, create a Recipient message to keep track of opens
            recipient_message = RecipientMessage.objects.create(message=self, recipient=email,
                token=make_token())
            domain = Site.objects.get_current().domain
            context = template.Context({"content_object": content_object, "domain": domain,
                "recipient": user_object if user_object else email })
            # render the body template with the given, template
            body = template.Template(self.body).render(context)
            for link in [m.group() for m in URL_REGEX.finditer(body)]:
                # for each unique link in the body, create a Message link to track the clicks
                ml = MessageLink.objects.create(recipient_message=recipient_message,
                    link=link, token=make_token())
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
            Sent.objects.create(message=self, recipient=email, email=msg.message())
    
    def unique_opens(self):
        opens = RecipientMessage.objects.filter(message=self, opens__gt=0).aggregate(
            models.Count("opens"))["opens__count"]
        return opens if opens else 0
    
    def __unicode__(self):
        return self.name

class RecipientMessage(models.Model):
    message = models.ForeignKey(Message)
    recipient = models.EmailField()
    token = models.CharField(max_length=30, editable=False, unique=True, db_index=True)
    opens = models.PositiveIntegerField(default=0, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class MessageLink(models.Model):
    recipient_message = models.ForeignKey(RecipientMessage)
    link = models.URLField(verify_exists=False)
    token = models.CharField(max_length=30, editable=False, unique=True, db_index=True)
    clicks = models.PositiveIntegerField(default=0, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class QueueManager(models.Manager):
    def send_ready_messages(self):
        now = datetime.datetime.now()
        for queued_message in self.filter(send_time__lte=now):
            queued_message.send()
            queued_message.delete()

class Queue(models.Model):
    message = models.ForeignKey(Message)
    content_type = models.ForeignKey(ContentType, verbose_name="content type", related_name="%(class)s")
    object_pk = models.PositiveIntegerField("object ID")
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    send_time = models.DateTimeField(db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = QueueManager()
    
    def send(self):
        return self.message.send(self.content_object)

class Stream(models.Model):
    slug = models.SlugField(db_index=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def _queued_messages(self, content_object):
        potential_messages = []
        for ab_test in ABTest.objects.filter(stream=self):
            potential_messages.append(ab_test.message)
            potential_messages.append(ab_test.test_message)
        return Queue.objects.filter(message__in=potential_messages, object_pk=content_object.pk,
            content_type=ContentType.objects.get_for_model(content_object))
    
    def enqueue(self, content_object, start, end):
        enqueued = []
        now = datetime.datetime.now()
        for ab_test in ABTest.objects.filter(stream=self):
            if not ab_test.is_enabled:
                continue
            message = ab_test.random_message()
            send_time = message.send_time(start, end)
            if send_time:
                if send_time <= now:
                    message.send(content_object)
                else:
                    enqueued.append(Queue.objects.create(message=message,
                        content_object=content_object, send_time=send_time))
        return enqueued
    
    def upqueue(self, content_object, start, end):
        upqueued = self._queued_messages(content_object)
        now = datetime.datetime.now()
        for queued_message in upqueued:
            message = queued_message.message
            send_time = message.send_time(start, end)
            if send_time <= now:
                queued_message.send()
                queued_message.delete()
            else:
                queued_message.send_time = send_time
                queued_message.save()
        return upqueued
    
    def dequeue(self, content_object):
        return self._queued_messages(content_object).delete()
    
    def __unicode__(self):
        return self.slug

class ABTest(models.Model):
    message = models.ForeignKey(Message, related_name="message")
    test_message = models.ForeignKey(Message, related_name="test_message", null=True, blank=True)
    test_percentage = models.PositiveIntegerField(default=0)
    is_enabled = models.BooleanField(default=True)
    stream = models.ForeignKey(Stream)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
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
