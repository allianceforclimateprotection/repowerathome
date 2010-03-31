"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from records.models import *
from rah.models import *


def create_test_users_and_action_tasks(object):
    """
    create a base set of users and action tasks and assign all of these variables to the given instance
    """
    object.u1 = User.objects.create(username='1', email='test@test.com')
    object.u2 = User.objects.create(username='2', email='test@test.net')
    object.a = Action.objects.create(name='test action', slug='test-action')
    object.at1 = ActionTask.objects.create(name='test action task 1', action=object.a, points=5, sequence=1)
    object.at2 = ActionTask.objects.create(name='test action task 2', action=object.a, points=10, sequence=2)
    object.at3 = ActionTask.objects.create(name='test action task 3', action=object.a, points=20, sequence=3)
    object.act1 = Activity.objects.get(slug='action_commitment')

class RecordManagerTest(TestCase):
    def setUp(self):
        create_test_users_and_action_tasks(self)
    
    def test_last_active(self):
        # TODO: Write test_last_active
        pass
    
    def test_get_chart_data(self):
        Record(user=self.u1, activity=self.act1, points=self.at1.points).save()
        Record(user=self.u1, activity=self.act1, points=self.at2.points).save()
        Record(user=self.u1, activity=self.act1, points=self.at3.points).save()
        
        chart_points = Record.objects.get_chart_data(self.u1)
        self.failUnlessEqual(len(chart_points), 1)
        self.failUnlessEqual(len(chart_points[0].records), 3)
        self.failUnlessEqual(chart_points[0].points, 35)
        
        point_data = [(chart_point.get_date_as_milli_from_epoch(), chart_point.points) for chart_point in chart_points]
        self.failUnlessEqual(len(point_data), 1)
        self.failUnlessEqual(point_data[0][1], 35)
    
    def test_user_records(self):        
        Record(user=self.u1, activity=self.act1, points=self.at1.points).save()
        Record(user=self.u1, activity=self.act1, points=self.at2.points).save()
        Record(user=self.u1, activity=self.act1, points=self.at3.points).save()
        self.failUnlessEqual(Record.objects.count(), 3)
        
        all_records = Record.objects.user_records(self.u1)
        self.failUnlessEqual(len(all_records), 3)
        
        two_records = Record.objects.user_records(self.u1, 2)
        self.failUnlessEqual(len(two_records), 2)
        
        # Make sure the order is correct (reverse cron)
        self.failUnless(all_records[0].created > all_records[1].created > all_records[2].created)
    
    def test_create_record(self):        
        # Add a record
        Record.objects.create_record(self.u1, self.act1, self.at1)
        self.failUnlessEqual(Record.objects.count(), 1)
        
        # Add another record
        Record.objects.create_record(self.u1, self.act1, self.at2)
        self.failUnlessEqual(Record.objects.count(), 2)
        
        # Add another record with activity slug
        Record.objects.create_record(self.u1, self.act1.slug, self.at2)
        self.failUnlessEqual(Record.objects.count(), 3)
    
    def test_void_record(self):    
        # Add some records
        self.failUnlessEqual(Record.objects.count(), 0)
        Record.objects.create_record(self.u1, self.act1, self.at1)
        Record.objects.create_record(self.u1, self.act1, self.at2)
        self.failUnlessEqual(Record.objects.count(), 2)
        
        # Void a record
        # Manager should automatically filter(void=False)
        Record.objects.void_record(self.u1, self.act1, self.at1)
        records = Record.objects.all()
        self.failUnlessEqual(records.count(), 1)
        self.failUnlessEqual(records[0].activity.id, self.act1.id)
        
        # Void record with activity slug
        Record.objects.void_record(self.u1, self.act1.slug, self.at2)
        self.failUnlessEqual(Record.objects.all().count(), 0)
        
    def test_total_points(self):
        Record.objects.create_record(self.u1, self.act1, self.at1)
        
        user = User.objects.get(pk=self.u1.id)
        self.failUnlessEqual(user.get_profile().total_points, 5)
        
        # self.u1.create_record(self.act1, self.at2)
        Record.objects.create_record(self.u1, self.act1, self.at2)
        
        user = User.objects.get(pk=self.u1.id)
        self.failUnlessEqual(user.get_profile().total_points, 15)
        
        # self.u1.create_record(self.act1, self.at3)
        Record.objects.create_record(self.u1, self.act1, self.at3)
        
        user = User.objects.get(pk=self.u1.id)
        self.failUnlessEqual(user.get_profile().total_points, 35)
        
        # self.u1.void_record(self.act1, self.at2)
        Record.objects.void_record(self.u1, self.act1, self.at2)
        
        user = User.objects.get(pk=self.u1.id)
        self.failUnlessEqual(user.get_profile().total_points, 25)
    
class RecordTest(TestCase):
    # fixtures = ['activity.json']
    def setUp(self):
        create_test_users_and_action_tasks(self)
    
    def test_render(self):
        r1 = Record.objects.create_record(self.u1, self.act1, self.at1)
        # TODO: test_render is a crappy test. Should probably use Client()
        # self.failUnless(100 < len(r1.render()) < 500)