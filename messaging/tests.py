import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from models import Message

class MessageTest(TestCase):
    fixtures = ["test_messaging.json"]
    
    def setUp(self):
        self.timeline = Message.objects.get(subject="timeline scale")
        
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
        
        
        