"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from rah.models import *
from records.models import *

def create_test_users_and_action_tasks(object):
    """
    create a base set of users and action tasks and assign all of these variables to the given instance
    """
    object.u1 = User.objects.create(username='1', email='test@test.com')
    object.u2 = User.objects.create(username='2', email='test@test.net')
    object.ac = ActionCat.objects.create(name='test action cat')
    object.a = Action.objects.create(name='test action', category=object.ac)
    object.at1 = ActionTask.objects.create(name='test action task 1', action=object.a, points=5, sequence=1)
    object.at2 = ActionTask.objects.create(name='test action task 2', action=object.a, points=10, sequence=2)
    object.at3 = ActionTask.objects.create(name='test action task 3', action=object.a, points=20, sequence=3)
    object.act1 = Activity.objects.create(slug='action_task_complete')

class RecordTest(TestCase):
    def setUp(self):
        create_test_users_and_action_tasks(self)

    def test_create_record(self):        
        # Add a record
        Record.objects.create_record(self.u1, self.act1, self.at1)
        self.failUnlessEqual(Record.objects.count(), 1)
    
        # Add another record
        Record.objects.create_record(self.u1, self.act1, self.at2)
        self.failUnlessEqual(Record.objects.count(), 2)
    
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