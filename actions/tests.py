import datetime

from django.contrib.auth.models import User
from django.core import management
from django.core.urlresolvers import reverse
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

    def test_process_commitment_card(self):
        event_date = datetime.datetime(2010, 1, 2)
        date_after_event = event_date + datetime.timedelta(1)
        date_before_event = event_date - datetime.timedelta(1)

        # Create an event cruft (the creator is automatically a guest)
        from events.models import Event, Guest
        from commitments.models import Survey, Commitment, Contributor
        survey = Survey.objects.create()
        event = Event.objects.create(creator=self.user, when=event_date, start=datetime.time(6, 0))
        guest = Guest.objects.get(pk=1)
        guest2 = Guest.objects.create(contributor=Contributor.objects.create(email="guest2@gmail.com"), event=event)

        # Create commitments
        Commitment.objects.create(contributor=guest.contributor, action=self.iwh, answer="D", question="1")
        Commitment.objects.create(contributor=guest.contributor, action=self.csp, answer="D", question="2")
        Commitment.objects.create(contributor=guest.contributor, action=self.cfw, answer="C", question="3")

        # Set last_login to be after the event
        # User has no entries in User Action Progress, so all actions and commitments should be applied
        response = self.client.post(reverse("login"), {"email":self.user.email, "password": "test"}, follow=True)
        self.client.get(reverse("logout"))
        self.failUnlessEqual(UserActionProgress.objects.filter(user=self.user).count(), 3)
        self.failUnlessEqual(UserActionProgress.objects.filter(user=self.user, date_committed__isnull=False).count(), 1)

        # Clear out UAP and login again
        # There should be nothing applied in UAP because the user's last_login time is after the updated time of the commitments
        UserActionProgress.objects.all().delete()
        response = self.client.post(reverse("login"), {"email":self.user.email, "password": "test"}, follow=True)
        self.client.get(reverse("logout"))
        self.failUnlessEqual(UserActionProgress.objects.filter(user=self.user).count(), 0)

        # Test that the commitments are added when a new user registers with an email that matches a guest with commitments
        Commitment.objects.create(contributor=guest2.contributor, action=self.iwh, answer="D", question="1")
        Commitment.objects.create(contributor=guest2.contributor, action=self.csp, answer="D", question="2")
        Commitment.objects.create(contributor=guest2.contributor, action=self.cfw, answer="C", question="3")
        # Register a rando user whose email does not match a guest
        reg_post = {"email": "ada@asd.com", "password1": "userpass", "password2": "userpass", "first_name": "guest2"}
        response = self.client.post(reverse("register"), reg_post, follow=True)
        self.client.get(reverse("logout"))
        user2 = User.objects.get(pk=2)
        self.failUnlessEqual(UserActionProgress.objects.filter(user=user2).count(), 0)
        # Register a user whose email matches a guest
        reg_post = {"email": guest2.contributor.email, "password1": "userpass", "password2": "userpass", "first_name": "guest2"}
        response = self.client.post(reverse("register"), reg_post, follow=True)
        self.client.get(reverse("logout"))
        user3 = User.objects.get(pk=3)
        self.failUnlessEqual(UserActionProgress.objects.filter(user=user3).count(), 3)
        self.failUnlessEqual(UserActionProgress.objects.filter(user=user3, date_committed__isnull=False).count(), 1)

        # User had committed to an action before the event, but said it was completed on the commitment card
        # reset last_login date to be before updated field on commitments
        # UserActionProgress.objects.all().delete()
        self.user.last_login = date_before_event
        self.user.save()
        # Commit and then change the event date to be in the future
        self.iwh.commit_for_user(self.user, datetime.datetime.now())
        event.when = datetime.datetime.now() + datetime.timedelta(1)
        event.save()
        response = self.client.post(reverse("login"), {"email":self.user.email, "password": "test"}, follow=True)
        self.failUnlessEqual(UserActionProgress.objects.filter(user=self.user).count(), 3)
        self.failUnlessEqual(UserActionProgress.objects.filter(user=self.user, date_committed__isnull=False).count(), 2)
        self.failUnlessEqual(UserActionProgress.objects.filter(user=self.user, is_completed=True).count(), 2)
        self.failUnlessEqual(UserActionProgress.objects.get(user=self.user, action=self.iwh).is_completed, True)

    def test_actions_by_status(self):
        self.iwh.complete_for_user(self.user)
        self.csp.complete_for_user(self.user)
        self.csp.commit_for_user(self.user, datetime.date.today())
        self.cfw.commit_for_user(self.user, datetime.date.today())

        actions = Action.objects.actions_by_status(self.user)
        self.failUnlessEqual(len(actions), Action.objects.all().count())
        self.failUnlessEqual(actions[0].committed, datetime.date.today())
        self.failUnlessEqual(actions.pop().completed, 1)
        self.failUnlessEqual(actions.pop().completed, 1)

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

class UserActionProgressTest(TestCase):
        fixtures = ["actions.json"]

        def setUp(self):
            self.user = User.objects.create_user(username="test", password="test", email="test@test.com")
            self.other = User.objects.create_user(username="other", password="other", email="other@test.com")
            self.iwh = Action.objects.get(slug="insulate-water-heater")
            self.csp = Action.objects.get(slug="eliminate-standby-vampire-power")
            self.cfw = Action.objects.get(slug="use-ceiling-fan-winter")

        def test_commitments_for_user(self):
            from datetime import date
            date_committed = date.today()
            UserActionProgress.objects.create(user=self.user, action=self.iwh, date_committed=date_committed)
            UserActionProgress.objects.create(user=self.other, action=self.csp, date_committed=date_committed)
            UserActionProgress.objects.create(user=self.user, action=self.cfw, date_committed=date_committed)

            commit_list = UserActionProgress.objects.commitments_for_user(self.user)
            self.failUnlessEqual(len(commit_list), 2)

            iwh_commitment, cfw_commitment = commit_list
            self.failUnlessEqual(iwh_commitment.action, self.iwh)
            self.failUnlessEqual(iwh_commitment.date_committed, date_committed)
            self.failUnlessEqual(cfw_commitment.action, self.cfw)
            self.failUnlessEqual(cfw_commitment.date_committed, date_committed)


