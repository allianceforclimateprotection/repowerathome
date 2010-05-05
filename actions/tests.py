import datetime

from django.contrib.auth.models import User
from django.core import management
from django.test import TestCase

from records.models import Record

from models import Action, UserActionProgress

class ActionTest(TestCase):
    fixtures = ["actions.json"]
    
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test", email="test@test.com")
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.cfw = Action.objects.get(slug="use-ceiling-fan-winter")
        
    def test_actions_by_status(self):
        self.iwh.complete_for_user(self.user)
        self.csp.complete_for_user(self.user)
        self.csp.commit_for_user(self.user, datetime.date.today())
        self.cfw.commit_for_user(self.user, datetime.date.today())
        
        actions, recommended, committed, completed = Action.objects.actions_by_status(self.user)
        sorted_actions = sorted(Action.objects.all(), key=lambda a: not a.has_illustration())
        self.failUnlessEqual(list(actions), sorted_actions)
        self.failUnlessEqual(recommended, 
            [a for a in sorted_actions if a not in [self.iwh, self.csp, self.cfw]])
        self.failUnlessEqual(committed, [self.cfw])
        self.failUnlessEqual(completed, [self.csp, self.iwh])
        
    def test_complete_for_user(self):
        self.failUnlessRaises(UserActionProgress.DoesNotExist, UserActionProgress.objects.get,
            user=self.user, action=self.iwh)
        self.failUnlessEqual(self.iwh.users_completed, 0)
        
        self.iwh.complete_for_user(self.user)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        
        uap = UserActionProgress.objects.get(user=self.user, action=self.iwh)
        self.failUnlessEqual(uap.is_completed, True)
        self.failUnlessEqual(self.iwh.users_completed, 1)
        records = Record.objects.filter(user=self.user, activity__slug="action_complete")
        self.failUnlessEqual(len(records), 1)
        record = records[0]
        self.failUnlessEqual(record.void, False)
        rao = record.content_objects.all()[0]
        self.failUnlessEqual(rao.content_object, self.iwh)
        
    def test_undo_for_user(self):
        self.test_complete_for_user()
        self.failUnlessEqual(self.iwh.users_completed, 1)
        
        self.iwh.undo_for_user(self.user)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        
        uap = UserActionProgress.objects.get(user=self.user, action=self.iwh)
        self.failUnlessEqual(uap.is_completed, False)
        self.failUnlessEqual(self.iwh.users_completed, 0)
        record = Record.objects.filter(user=self.user, activity__slug="action_complete")
        self.failUnlessEqual(list(record), [])
        
    def test_commit_for_user(self):
        self.failUnlessRaises(UserActionProgress.DoesNotExist, UserActionProgress.objects.get,
            user=self.user, action=self.iwh)
        self.failUnlessEqual(self.iwh.users_committed, 0)
        today = datetime.date.today()
        
        self.iwh.commit_for_user(self.user, today)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        
        uap = UserActionProgress.objects.get(user=self.user, action=self.iwh)
        self.failUnlessEqual(uap.date_committed, today)
        self.failUnlessEqual(self.iwh.users_committed, 1)
        records = Record.objects.filter(user=self.user, activity__slug="action_commitment")
        self.failUnlessEqual(len(records), 1)
        record = records[0]
        self.failUnlessEqual(record.void, False)
        rao = record.content_objects.all()[0]
        self.failUnlessEqual(rao.content_object, self.iwh)
        
    def test_cancel_for_user(self):
        self.test_commit_for_user()
        self.failUnlessEqual(self.iwh.users_committed, 1)
        
        self.iwh.cancel_for_user(self.user)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        
        uap = UserActionProgress.objects.get(user=self.user, action=self.iwh)
        self.failUnlessEqual(uap.date_committed, None)
        self.failUnlessEqual(self.iwh.users_committed, 0)
        record = Record.objects.filter(user=self.user, activity__slug="action_commitment")
        self.failUnlessEqual(list(record), [])
        
    def test_action_completed_aggregate_signal(self):
        user_2 = User.objects.create_user(username="test_2", password="test", email="test_2@test.com")
        self.failUnlessEqual(self.iwh.users_completed, 0)
        self.failUnlessEqual(self.csp.users_completed, 0)
        
        self.iwh.complete_for_user(self.user)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_completed, 1)
        self.failUnlessEqual(self.csp.users_completed, 0)
        
        self.csp.complete_for_user(user_2)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_completed, 1)
        self.failUnlessEqual(self.csp.users_completed, 1)
        
        self.iwh.complete_for_user(user_2)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_completed, 2)
        self.failUnlessEqual(self.csp.users_completed, 1)
        
        self.csp.complete_for_user(self.user)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_completed, 2)
        self.failUnlessEqual(self.csp.users_completed, 2)
        
        self.csp.complete_for_user(user_2)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_completed, 2)
        self.failUnlessEqual(self.csp.users_completed, 2)
        
        self.csp.undo_for_user(user_2)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_completed, 2)
        self.failUnlessEqual(self.csp.users_completed, 1)
        
        self.csp.undo_for_user(self.user)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_completed, 2)
        self.failUnlessEqual(self.csp.users_completed, 0)
        
    def test_action_committed_aggregate_signal(self):
        user_2 = User.objects.create_user(username="test_2", password="test", email="test_2@test.com")
        today = datetime.date.today()
        self.failUnlessEqual(self.iwh.users_committed, 0)
        self.failUnlessEqual(self.csp.users_committed, 0)

        self.iwh.commit_for_user(self.user, today)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_committed, 1)
        self.failUnlessEqual(self.csp.users_committed, 0)

        self.csp.commit_for_user(user_2, today)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_committed, 1)
        self.failUnlessEqual(self.csp.users_committed, 1)

        self.iwh.commit_for_user(user_2, today)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_committed, 2)
        self.failUnlessEqual(self.csp.users_committed, 1)

        self.csp.commit_for_user(self.user, today)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_committed, 2)
        self.failUnlessEqual(self.csp.users_committed, 2)

        self.csp.commit_for_user(user_2, today)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_committed, 2)
        self.failUnlessEqual(self.csp.users_committed, 2)
        
        self.csp.cancel_for_user(user_2)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_committed, 2)
        self.failUnlessEqual(self.csp.users_committed, 1)
        
        self.csp.cancel_for_user(self.user)
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
        self.failUnlessEqual(self.iwh.users_committed, 2)
        self.failUnlessEqual(self.csp.users_committed, 0)
        
        