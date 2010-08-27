import datetime

from django.core.urlresolvers import reverse
from django.core import mail
from django.test import TestCase
from django.test.client import Client

from messaging.models import Message, Stream, Queue, ABTest, Sent

from models import User, Event

class MessageSendTimeTest(TestCase):
    fixtures = ["test_messaging.json"]
    
    def test_send_immediately(self):
        send_immediately = Message.objects.get(name="send immediately")
        before = datetime.datetime.now()
        send_time = send_immediately.send_time(start=datetime.datetime.now())
        after = datetime.datetime.now()
        self.failUnless(before <= send_time)
        self.failUnless(send_time <= after)
    
    def test_send_after_start(self):
        start = datetime.datetime(2010, 7, 1, 18, 00)
        end = datetime.datetime(2010, 7, 8, 18, 00)
        after_start = Message.objects.get(name="after start")
        
        self.failUnlessEqual(after_start.send_time(start, end), datetime.datetime(2010, 7, 2, 18, 00))
        
        after_start.x_value = 192
        self.failUnlessEqual(after_start.send_time(start, end), None)
        
    def test_send_before_end(self):
        start = datetime.datetime(2010, 7, 1, 18, 00)
        end = datetime.datetime(2010, 7, 5, 18, 00)
        before_end = Message.objects.get(name="before end")
        
        self.failUnlessEqual(before_end.send_time(start, end), datetime.datetime(2010, 7, 2, 18, 00))
        
        before_end.x_value = 180
        self.failUnlessEqual(before_end.send_time(start, end), None)
        
    def test_send_after_end(self):
        start = datetime.datetime(2010, 7, 1, 18, 00)
        end = datetime.datetime(2010, 7, 10, 20, 30)
        after_end = Message.objects.get(name="after end")
        
        self.failUnlessEqual(after_end.send_time(start, end), datetime.datetime(2010, 7, 17, 20, 30))
        
        after_end.x_value = 36
        self.failUnlessEqual(after_end.send_time(start, end), datetime.datetime(2010, 7, 12, 8, 30))
        
    def test_send_timeline_scale(self):
        start = datetime.datetime(2010, 7, 1, 18, 00)
        end = datetime.datetime(2010, 7, 20, 20, 30)
        timeline = Message.objects.get(name="timeline scale")
        
        self.failUnlessEqual(timeline.send_time(start, end), datetime.datetime(2010, 7, 11, 7, 15))
        
        timeline.x_value = 0
        self.failUnlessEqual(timeline.send_time(start, end), datetime.datetime(2010, 7, 1, 18, 00))
        
    def test_send_with_time_snap(self):
        start = datetime.datetime(2010, 7, 1, 18, 00)
        end = datetime.datetime(2010, 7, 8, 18, 00)
        time_snap = Message.objects.get(name="time snap")
        
        self.failUnlessEqual(time_snap.send_time(start, end), datetime.datetime(2010, 7, 2, 11, 15))
        
    def test_send_with_duration_minimum(self):
        start = datetime.datetime(2010, 7, 1, 18, 00)
        end = datetime.datetime(2010, 7, 4, 18, 00)
        minimum_duration = Message.objects.get(name="minimum duration")
        
        self.failUnlessEqual(minimum_duration.send_time(start, end), None)
        
        minimum_duration.minimum_duration = 24
        self.failUnlessEqual(minimum_duration.send_time(start, end), datetime.datetime(2010, 7, 3, 18, 00))
        
class MessageRecipientTest(TestCase):
    fixtures = ["test_messaging.json"]
    
    def setUp(self):
        self.event = Event.objects.get(pk=1)
        self.joe = User.objects.get(email="joe@email.com")
        self.matt = User.objects.get(email="matt@email.com")
        self.larry = User.objects.get(email="larry@email.com")
        
    def test_recipient_email(self):
        after_end = Message.objects.get(name="after end")
        recipients = after_end.recipients(self.event)
        self.failUnlessEqual(recipients, [("joe@email.com", None)])
        
    def test_recipient_object(self):
        after_start = Message.objects.get(name="after start")
        recipients = after_start.recipients(self.event)
        self.failUnlessEqual(recipients, [("joe@email.com", self.joe)])
        
    def test_recipient_email_list(self):
        timeline = Message.objects.get(name="timeline scale")
        recipients = timeline.recipients(self.event)
        self.failUnlessEqual(recipients, [("joe@email.com", None), 
            ("matt@email.com", None), ("larry@email.com", None)])
        
    def test_recipient_object_list(self):
        before_end = Message.objects.get(name="before end")
        recipients = before_end.recipients(self.event)
        self.failUnlessEqual(recipients, [("joe@email.com", self.joe), 
            ("matt@email.com", self.matt), ("larry@email.com", self.larry)])
            
    def test_lambda(self):
        lambda_recipient = Message.objects.get(name="lambda recipient")
        recipients = lambda_recipient.recipients(self.event)
        self.failUnlessEqual(recipients, [("test@gmail.com", None), ("test@yahoo.com", None)])
            
class MessageTest(TestCase):
    fixtures = ["test_messaging.json"]
    
    def setUp(self):
        self.after_start = Message.objects.get(name="after start")
        self.before_end = Message.objects.get(name="before end")
        self.after_end = Message.objects.get(name="after end")
        self.timeline_scale = Message.objects.get(name="timeline scale")
        self.now = Message.objects.get(name="now")
        self.time_snap = Message.objects.get(name="time snap")
        
        self.test = Stream.objects.get(slug="test")
        self.dummy = Stream.objects.get(slug="dummy")
        
    def test_related_streams(self):
        self.failUnlessEqual(list(self.after_start.related_streams()), [self.test, self.dummy])
        self.failUnlessEqual(list(self.before_end.related_streams()), [self.test, self.dummy])
        self.failUnlessEqual(list(self.after_end.related_streams()), [self.test])
        self.failUnlessEqual(list(self.timeline_scale.related_streams()), [])
        self.failUnlessEqual(list(self.now.related_streams()), [self.test])
        self.failUnlessEqual(list(self.time_snap.related_streams()), [])
            
class QueueTest(TestCase):
    fixtures = ["test_queue.json"]
        
    def test_find_batchable_messages(self):
        self.normal = Queue.objects.get(pk=1)
        self.time_snap = Queue.objects.get(pk=4)
        self.batch_1 = Queue.objects.get(pk=5)
        self.batch_2 = Queue.objects.get(pk=6)
        self.batch_3 = Queue.objects.get(pk=7)
        self.test_batch = Queue.objects.get(pk=8)
        
        self.failUnlessEqual(self.normal.find_batchable_messages(), None)
        self.failUnlessEqual(list(self.batch_1.find_batchable_messages()), [self.batch_2, self.test_batch])
        self.failUnlessEqual(list(self.batch_2.find_batchable_messages()), [self.batch_1, self.test_batch])
        self.failUnlessEqual(self.batch_3.find_batchable_messages(), None)
        self.failUnlessEqual(list(self.test_batch.find_batchable_messages()), [self.batch_1, self.batch_2])
        
    def test_send_ready_messages(self):
        sent = Queue.objects.send_ready_messages()
        
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["joe@email.com"])
        self.failUnlessEqual(email.subject, "normal message")
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["matt@email.com"])
        self.failUnlessEqual(email.subject, "normal message")
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["matt@email.com"])
        self.failUnlessEqual(email.subject, "batch message")
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["joe@email.com"])
        self.failUnlessEqual(email.subject, "batch message")
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["matt@email.com"])
        self.failUnlessEqual(email.subject, "time snap message")
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["joe@email.com"])
        self.failUnlessEqual(email.subject, "normal message")
        
        self.failUnlessEqual(sent, list(Sent.objects.all()))
        
        self.failUnlessEqual(sent[0].message.subject, "normal message")
        self.failUnlessEqual(sent[0].recipient, "joe@email.com")
        self.failUnlessEqual(sent[1].message.subject, "time snap message")
        self.failUnlessEqual(sent[1].recipient, "matt@email.com")
        self.failUnlessEqual(sent[2].message.subject, "batch message")
        self.failUnlessEqual(sent[2].recipient, "joe@email.com")
        self.failUnlessEqual(sent[3].message.subject, "batch message")
        self.failUnlessEqual(sent[3].recipient, "matt@email.com")
        self.failUnlessEqual(sent[4].message.subject, "normal message")
        self.failUnlessEqual(sent[4].recipient, "matt@email.com")
        self.failUnlessEqual(sent[5].message.subject, "normal message")
        self.failUnlessEqual(sent[5].recipient, "joe@email.com")
            
class StreamTest(TestCase):
    fixtures = ["test_messaging.json"]
    
    def setUp(self):
        self.stream = Stream.objects.get(slug="test")
        self.event = Event.objects.get(pk=1)
        self.before_end = Message.objects.get(name="before end")
        self.after_end = Message.objects.get(name="after end")
    
    def test_enqueue(self):
        start = datetime.datetime.now()
        end = start + datetime.timedelta(days=7)
        self.failUnlessEqual(Queue.objects.all().count(), 0)
        queued = self.stream.enqueue(self.event, start, end)
        self.failUnlessEqual(Queue.objects.all().count(), 2)
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["joe@email.com"])
        self.failUnlessEqual(email.subject, "now")
        self.failUnlessEqual(len(queued), 2)
        
        self.failUnlessEqual(queued[0].message, self.before_end)
        self.failUnlessEqual(queued[0].content_object, self.event)
        self.failUnlessEqual(queued[0].send_time, end - datetime.timedelta(days=3))
        
        self.failUnlessEqual(queued[1].message, self.after_end)
        self.failUnlessEqual(queued[1].content_object, self.event)
        self.failUnlessEqual(queued[1].send_time, end + datetime.timedelta(days=7))
        
    def test_upqueue(self):
        self.test_enqueue()
        
        start = datetime.datetime.now()
        end = start + datetime.timedelta(days=14)
        self.failUnlessEqual(Queue.objects.all().count(), 2)
        queued = self.stream.upqueue(self.event, start, end)
        self.failUnlessEqual(Queue.objects.all().count(), 2)
        self.failUnlessEqual(len(queued), 2)
        
        self.failUnlessEqual(queued[0].message, self.before_end)
        self.failUnlessEqual(queued[0].content_object, self.event)
        self.failUnlessEqual(queued[0].send_time, end - datetime.timedelta(days=3))
        
        self.failUnlessEqual(queued[1].message, self.after_end)
        self.failUnlessEqual(queued[1].content_object, self.event)
        self.failUnlessEqual(queued[1].send_time, end + datetime.timedelta(days=7))
        
    def test_dequeue(self):
        self.test_enqueue()
        
        self.failUnlessEqual(Queue.objects.all().count(), 2)
        self.stream.dequeue(self.event)
        self.failUnlessEqual(Queue.objects.all().count(), 0)
        
    def test_blacklisted_emails(self):
        self.failUnlessEqual(self.stream.blacklisted_emails(), ["larry@email.com"])
        
class ABTestTest(TestCase):
    fixtures = ["test_messaging.json"]
    
    def setUp(self):
        self.ab_test_1 = ABTest.objects.get(pk=1)
        self.ab_test_2 = ABTest.objects.get(pk=2)
        self.ab_test_3 = ABTest.objects.get(pk=3)
        self.ab_test_4 = ABTest.objects.get(pk=4)
        self.after_start = Message.objects.get(name="after start")
        self.before_end = Message.objects.get(name="before end")
        self.after_end = Message.objects.get(name="after end")
        self.now = Message.objects.get(name="now")
    
    def test_random_message(self):
        control_count = 0
        test_count = 0
        for index in range(0, 10000):
            message = self.ab_test_4.random_message()
            if message == self.after_start:
                control_count += 1
            elif message == self.before_end:
                test_count += 1
        message = "This unit test has some randomness to it, and might fail from time to time. \
            Try running again."
        self.failUnless(abs(control_count-7500)/7500 < 0.1, message)
        self.failUnless(abs(test_count-2500)/2500 < 0.1, message)
        
    def test_potential_message_by_message(self):
        messages = ABTest.objects.potential_messages(message=self.after_start)
        self.failUnlessEqual(messages, [self.after_start, self.before_end])