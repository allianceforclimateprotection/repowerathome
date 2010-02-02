"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from rah.models import *

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

class UserTest(TestCase):
    def setUp(self):
        self.u1 = User(username='1', email='test@test.com')
        self.u2 = User(username='2', email='test@test.net', first_name='first')
        self.u3 = User(username='3', email='test@test.org', last_name='last')
        self.u4 = User(username='4', email='test@test.edu', first_name='first', last_name='last')

    def test_get_name(self):
        self.failUnlessEqual(self.u1.get_name(), 'test@test.com')
        self.failUnlessEqual(self.u2.get_name(), 'first')
        self.failUnlessEqual(self.u3.get_name(), 'last')
        self.failUnlessEqual(self.u4.get_name(), 'first last')
        
class UserManagerTest(TestCase):
    def setUp(self):
        create_test_users_and_action_tasks(self)


class ActionTest(TestCase):
    def setUp(self):
        create_test_users_and_action_tasks(self)
    
    def test_no_user_completes(self):
        action = Action.objects.actions_by_completion_status(self.u1)[0][0]
        
        self.failUnlessEqual(action.total_tasks, 3)
        self.failUnlessEqual(action.user_completes, 0)
        
    def test_one_user_complete(self):
        Record.objects.create(activity=self.at1, user=self.u1)
        
        action = Action.objects.actions_by_completion_status(self.u1)[0][0]
        
        self.failUnlessEqual(action.total_tasks, 3)
        self.failUnlessEqual(action.user_completes, 1)
        
    def test_all_user_completes(self):
        Record.objects.create(activity=self.at1, user=self.u1)
        Record.objects.create(activity=self.at2, user=self.u1)
        Record.objects.create(activity=self.at3, user=self.u1)

        action = Action.objects.actions_by_completion_status(self.u1)[0][0]

        self.failUnlessEqual(action.total_tasks, 3)
        self.failUnlessEqual(action.user_completes, 3)
    
    def test_partial_users_completes(self):
        Record.objects.create(activity=self.at1, user=self.u1)
        Record.objects.create(activity=self.at2, user=self.u2)
        Record.objects.create(activity=self.at3, user=self.u1)

        action1 = Action.objects.actions_by_completion_status(self.u1)[0][0]
        action2 = Action.objects.actions_by_completion_status(self.u2)[0][0]

        self.failUnlessEqual(action1.total_tasks, 3)
        self.failUnlessEqual(action1.user_completes, 2)
        self.failUnlessEqual(action2.total_tasks, 3)
        self.failUnlessEqual(action2.user_completes, 1)
        
    def test_all_users_completes(self):
        Record.objects.create(activity=self.at1, user=self.u1)
        Record.objects.create(activity=self.at2, user=self.u1)
        Record.objects.create(activity=self.at3, user=self.u1)
        Record.objects.create(activity=self.at1, user=self.u2)
        Record.objects.create(activity=self.at2, user=self.u2)
        Record.objects.create(activity=self.at3, user=self.u2)

        action1 = Action.objects.actions_by_completion_status(self.u1)[0][0]
        action2 = Action.objects.actions_by_completion_status(self.u2)[0][0]

        self.failUnlessEqual(action1.total_tasks, 3)
        self.failUnlessEqual(action1.user_completes, 3)
        self.failUnlessEqual(action2.total_tasks, 3)
        self.failUnlessEqual(action2.user_completes, 3)
        
    def test_action_total_points(self):
        self.failUnlessEqual(self.a.total_points, 35)
        
    def test_action_number_of_tasks(self):
        self.failUnlessEqual(self.a.total_tasks, 3)
        
    def test_action_tasks_by_user(self):
        Record.objects.create(activity=self.at1, user=self.u1)
        Record.objects.create(activity=self.at3, user=self.u1)

        action_tasks = self.a.get_action_tasks_by_user(self.u1)

        self.failIfEqual(action_tasks[0].is_complete, None)
        self.failUnlessEqual(action_tasks[1].is_complete, None)
        self.failIfEqual(action_tasks[2].is_complete, None)
        
    def test_users_with_completes(self):
        self.failUnlessEqual(self.a.users_with_completes()[0], 0)
        self.failUnlessEqual(self.a.users_with_completes()[2], 0)

        Record.objects.create(activity=self.at1, user=self.u1)
        action = Action.objects.get(id=self.a.id)
        self.failUnlessEqual(action.users_with_completes()[0], 1)
        self.failUnlessEqual(action.users_with_completes()[2], 0)

        Record.objects.create(activity=self.at2, user=self.u1)
        Record.objects.create(activity=self.at1, user=self.u2)
        action = Action.objects.get(id=self.a.id)
        self.failUnlessEqual(action.users_with_completes()[0], 2)
        self.failUnlessEqual(action.users_with_completes()[2], 0)

        Record.objects.create(activity=self.at3, user=self.u1)
        Record.objects.create(activity=self.at2, user=self.u2)
        action = Action.objects.get(id=self.a.id)
        self.failUnlessEqual(action.users_with_completes()[0], 1)
        self.failUnlessEqual(action.users_with_completes()[2], 1)

        Record.objects.create(activity=self.at3, user=self.u2)
        action = Action.objects.get(id=self.a.id)
        self.failUnlessEqual(action.users_with_completes()[0], 0)
        self.failUnlessEqual(action.users_with_completes()[2], 2)
        
class ProfileTest(TestCase):
    def setUp(self):
        test_user_email    = "test@test.com"
        user               = User(username='1', id=1, email=test_user_email)
        self.profile       = Profile.objects.create(user=user)
        self.expected_url  = "http://www.gravatar.com/avatar/b642b4217b34b1e8d3bd915fc65c4452?r=g&d=identicon"
        self.expected_hash = "b642b4217b34b1e8d3bd915fc65c4452"
        
    def test_get_gravatar_url(self):
        url = self.profile.get_gravatar_url()
        self.failUnlessEqual(url, self.expected_url)
    
    def test_email_hash(self):
        email_hash = self.profile._email_hash()
        self.failUnlessEqual(email_hash, self.expected_hash)