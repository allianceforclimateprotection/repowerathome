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
    object.at1 = ActionTask.objects.create(name='test action task 1', action=object.a, points=10, sequence=1)
    object.at2 = ActionTask.objects.create(name='test action task 2', action=object.a, points=10, sequence=2)
    object.at3 = ActionTask.objects.create(name='test action task 3', action=object.a, points=10, sequence=3)

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
        
    def test_set_email(self):
        self.u1.set_email('normal_email@test.com')
        self.failUnlessEqual(len(self.u1.username), 30)
        self.failUnlessEqual(self.u1.email, 'normal_email@test.com')

class ActionTest(TestCase):
    def setUp(self):
        create_test_users_and_action_tasks(self)
    
    def test_no_user_completes(self):
        action = Action.get_actions_with_tasks_and_user_completes_for_user(self.u1)[0]
        
        self.failUnlessEqual(action.tasks, 3)
        self.failUnlessEqual(action.user_completes, 0)
        
    def test_one_user_complete(self):
        UserActionTask.objects.create(action_task=self.at1, user=self.u1)
        
        action = Action.get_actions_with_tasks_and_user_completes_for_user(self.u1)[0]
        
        self.failUnlessEqual(action.tasks, 3)
        self.failUnlessEqual(action.user_completes, 1)
        
    def test_all_user_completes(self):
        UserActionTask.objects.create(action_task=self.at1, user=self.u1)
        UserActionTask.objects.create(action_task=self.at2, user=self.u1)
        UserActionTask.objects.create(action_task=self.at3, user=self.u1)

        action = Action.get_actions_with_tasks_and_user_completes_for_user(self.u1)[0]

        self.failUnlessEqual(action.tasks, 3)
        self.failUnlessEqual(action.user_completes, 3)
    
    def test_partial_users_completes(self):
        UserActionTask.objects.create(action_task=self.at1, user=self.u1)
        UserActionTask.objects.create(action_task=self.at2, user=self.u2)
        UserActionTask.objects.create(action_task=self.at3, user=self.u1)

        action1 = Action.get_actions_with_tasks_and_user_completes_for_user(self.u1)[0]
        action2 = Action.get_actions_with_tasks_and_user_completes_for_user(self.u2)[0]

        self.failUnlessEqual(action1.tasks, 3)
        self.failUnlessEqual(action1.user_completes, 2)
        self.failUnlessEqual(action2.tasks, 3)
        self.failUnlessEqual(action2.user_completes, 1)
        
    def test_all_users_completes(self):
        UserActionTask.objects.create(action_task=self.at1, user=self.u1)
        UserActionTask.objects.create(action_task=self.at2, user=self.u1)
        UserActionTask.objects.create(action_task=self.at3, user=self.u1)
        UserActionTask.objects.create(action_task=self.at1, user=self.u2)
        UserActionTask.objects.create(action_task=self.at2, user=self.u2)
        UserActionTask.objects.create(action_task=self.at3, user=self.u2)

        action1 = Action.get_actions_with_tasks_and_user_completes_for_user(self.u1)[0]
        action2 = Action.get_actions_with_tasks_and_user_completes_for_user(self.u2)[0]

        self.failUnlessEqual(action1.tasks, 3)
        self.failUnlessEqual(action1.user_completes, 3)
        self.failUnlessEqual(action2.tasks, 3)
        self.failUnlessEqual(action2.user_completes, 3)
        
class ActionTaskTest(TestCase):
    def setUp(self):
        create_test_users_and_action_tasks(self)

    def test_action_task_completion_status(self):
        UserActionTask.objects.create(action_task=self.at1, user=self.u1)
        UserActionTask.objects.create(action_task=self.at3, user=self.u1)
        
        action_tasks = ActionTask.get_action_tasks_by_action_and_user(self.a, self.u1)
        
        self.failIfEqual(action_tasks[0].completed, None)
        self.failUnlessEqual(action_tasks[1].completed, None)
        self.failIfEqual(action_tasks[2].completed, None)
        
        
    