import datetime

from django.contrib.auth.models import User
from django.core import management
from django.test import TestCase

from records.models import Record

from models import Action, UserActionProgress

class ActionTest(TestCase):
    fixtures = ["action.json"]
    
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test", email="test@test.com")
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="cut-standby-power")
        self.cfw = Action.objects.get(slug="use-ceiling-fan-winter")
        
    def test_actions_by_status(self):
        self.iwh.complete_for_user(self.user)
        self.csp.complete_for_user(self.user)
        self.csp.commit_for_user(self.user, datetime.date.today())
        self.cfw.commit_for_user(self.user, datetime.date.today())
        
        actions, recommended, committed, completed = Action.objects.actions_by_status(self.user)
        self.failUnlessEqual(list(actions), list(Action.objects.all()))
        self.failUnlessEqual(recommended, 
            [a for a in Action.objects.all() if a not in [self.iwh, self.csp, self.cfw]])
        self.failUnlessEqual(committed, [self.cfw])
        self.failUnlessEqual(completed, [self.iwh, self.csp])
        
    def test_complete_for_user(self):
        self.failUnlessRaises(UserActionProgress.DoesNotExist, UserActionProgress.objects.get,
            user=self.user, action=self.iwh)
        self.iwh.complete_for_user(self.user)
        uap = UserActionProgress.objects.get(user=self.user, action=self.iwh)
        self.failUnlessEqual(uap.is_completed, True)
        records = Record.objects.filter(user=self.user, activity__slug="action_complete")
        self.failUnlessEqual(len(records), 1)
        record = records[0]
        self.failUnlessEqual(record.void, False)
        rao = record.content_objects.all()[0]
        self.failUnlessEqual(rao.content_object, self.iwh)
        
    def test_undo_for_user(self):
        self.test_complete_for_user()
        
        self.iwh.undo_for_user(self.user)
        uap = UserActionProgress.objects.get(user=self.user, action=self.iwh)
        self.failUnlessEqual(uap.is_completed, False)
        record = Record.objects.filter(user=self.user, activity__slug="action_complete")
        self.failUnlessEqual(list(record), [])
        