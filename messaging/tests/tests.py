import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from messaging.models import Message

from models import User, Event

class MessageSendTimeTest(TestCase):
    fixtures = ["test_messaging.json"]
    
    def test_send_after_start(self):
        start = datetime.datetime(2010, 7, 1, 18, 00)
        end = datetime.datetime(2010, 7, 8, 18, 00)
        after_start = Message.objects.get(subject="after start")
        
        self.failUnlessEqual(after_start.send_time(start, end), datetime.datetime(2010, 7, 2, 18, 00))
        
        after_start.delta_value = 192
        self.failUnlessEqual(after_start.send_time(start, end), None)
        
    def test_send_before_end(self):
        start = datetime.datetime(2010, 7, 1, 18, 00)
        end = datetime.datetime(2010, 7, 5, 18, 00)
        before_end = Message.objects.get(subject="before end")
        
        self.failUnlessEqual(before_end.send_time(start, end), datetime.datetime(2010, 7, 2, 18, 00))
        
        before_end.delta_value = 180
        self.failUnlessEqual(before_end.send_time(start, end), None)
        
    def test_send_after_end(self):
        start = datetime.datetime(2010, 7, 1, 18, 00)
        end = datetime.datetime(2010, 7, 10, 20, 30)
        after_end = Message.objects.get(subject="after end")
        
        self.failUnlessEqual(after_end.send_time(start, end), datetime.datetime(2010, 7, 17, 20, 30))
        
        after_end.delta_value = 36
        self.failUnlessEqual(after_end.send_time(start, end), datetime.datetime(2010, 7, 12, 8, 30))
        
    def test_send_timeline_scale(self):
        start = datetime.datetime(2010, 7, 1, 18, 00)
        end = datetime.datetime(2010, 7, 20, 20, 30)
        timeline = Message.objects.get(subject="timeline scale")
        
        self.failUnlessEqual(timeline.send_time(start, end), datetime.datetime(2010, 7, 11, 7, 15))
        
        timeline.delta_value = 0
        self.failUnlessEqual(timeline.send_time(start, end), datetime.datetime(2010, 7, 1, 18, 00))
        
class MessageRecipientTest(TestCase):
    fixtures = ["test_messaging.json"]
    
    def setUp(self):
        self.event = Event.objects.get(pk=1)
        self.joe = User.objects.get(email="joe@email.com")
        self.matt = User.objects.get(email="matt@email.com")
        self.larry = User.objects.get(email="larry@email.com")
        
    def test_recipient_email(self):
        after_end = Message.objects.get(subject="after end")
        recipients = after_end.recipients(self.event)
        self.failUnlessEqual(recipients, [("joe@email.com", None)])
        
    def test_recipient_object(self):
        after_start = Message.objects.get(subject="after start")
        recipients = after_start.recipients(self.event)
        self.failUnlessEqual(recipients, [("joe@email.com", self.joe)])
        
    def test_recipient_email_list(self):
        timeline = Message.objects.get(subject="timeline scale")
        recipients = timeline.recipients(self.event)
        self.failUnlessEqual(recipients, [("joe@email.com", None), 
            ("matt@email.com", None), ("larry@email.com", None)])
        
    def test_recipient_object_list(self):
        before_end = Message.objects.get(subject="before end")
        recipients = before_end.recipients(self.event)
        self.failUnlessEqual(recipients, [("joe@email.com", self.joe), 
            ("matt@email.com", self.matt), ("larry@email.com", self.larry)])
        
        