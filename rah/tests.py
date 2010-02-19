from django.test import TestCase
from django.contrib.auth.models import AnonymousUser

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

class ChartPoint(TestCase):
    def test_add_record(self):
        pass
    
    def get_date_as_milli_from_epoch(self):
        pass

class UserTest(TestCase):
    def setUp(self):
        create_test_users_and_action_tasks(self)
    
    def test_get_chart_data(self):
        Record(user=self.u1, activity=self.at1, points=self.at1.points).save()
        Record(user=self.u1, activity=self.at2, points=self.at2.points).save()
        Record(user=self.u1, activity=self.at3, points=self.at3.points).save()
        
        chart_points = self.u1.get_chart_data()
        self.failUnlessEqual(len(chart_points), 1)
        self.failUnlessEqual(len(chart_points[0].records), 3)
        self.failUnlessEqual(chart_points[0].points, 35)
        
        point_data = [(chart_point.get_date_as_milli_from_epoch(), chart_point.points) for chart_point in chart_points]
        self.failUnlessEqual(len(point_data), 1)
        self.failUnlessEqual(point_data[0][1], 35)
    
    def test_get_latest_records(self):        
        Record(user=self.u1, activity=self.at1, points=self.at1.points).save()
        Record(user=self.u1, activity=self.at2, points=self.at2.points).save()
        Record(user=self.u1, activity=self.at3, points=self.at3.points).save()
        self.failUnlessEqual(Record.objects.count(), 3)
        
        all_records = self.u1.get_latest_records()
        self.failUnlessEqual(len(all_records), 3)
        
        two_records = self.u1.get_latest_records(2)
        self.failUnlessEqual(len(two_records), 2)
        
        # Make sure the order is correct
        self.failUnless(all_records[0].created < all_records[1].created < all_records[2].created)
    
    def test_record_activity(self):        
        # User should have zero points
        self.failUnlessEqual(self.u1.get_profile().total_points, 0)
        
        # Add a record
        self.u1.record_activity(self.at1)
        self.failUnlessEqual(Record.objects.count(), 1)
        self.failUnlessEqual(self.u1.get_profile().total_points, self.at1.points)
        
        # Add another record
        self.u1.record_activity(self.at2)
        self.failUnlessEqual(Record.objects.count(), 2)
        
    def test_unrecord_activity(self):    
        # Add some records
        self.failUnlessEqual(Record.objects.count(), 0)
        Record(user=self.u1, activity=self.at1, points=self.at1.points).save()
        Record(user=self.u1, activity=self.at2, points=self.at1.points).save()
        self.failUnlessEqual(Record.objects.count(), 2)
        
        # Make sure the right record was deleted
        self.u1.unrecord_activity(self.at1)
        self.failUnlessEqual(Record.objects.count(), 1)
        self.failUnlessEqual(Record.objects.all()[0].activity.id, self.at2.id)
        
    def test_record_action_task(self):        
        self.u1.record_activity(self.at1)
        record = Record.objects.get(user=self.u1, activity=self.at1)
        self.failUnlessEqual(record.points, self.at1.points)
        self.failUnlessEqual(record.message, self.at1.name)
        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 1)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 1)
        self.failUnlessEqual(action.users_completed, 0)
        
    def test_complete_action(self):        
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 0)
        self.failUnlessEqual(action.users_completed, 0)
        
        self.u1.record_activity(self.at1)

        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 1)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 1)
        self.failUnlessEqual(action.users_completed, 0)
        
        self.u1.record_activity(self.at2)
        
        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 2)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 1)
        self.failUnlessEqual(action.users_completed, 0)
        
        self.u1.record_activity(self.at3)
        
        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 3)
        self.failUnlessEqual(uap.is_completed, 1)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 0)
        self.failUnlessEqual(action.users_completed, 1)
        
    def test_multi_user_complete_action(self):        
        self.u1.record_activity(self.at1)
    
        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 1)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 1)
        self.failUnlessEqual(action.users_completed, 0)
        
        self.u2.record_activity(self.at1)
        
        uap = UserActionProgress.objects.get(user=self.u2, action=self.a)
        self.failUnlessEqual(uap.user_completes, 1)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 2)
        self.failUnlessEqual(action.users_completed, 0)
        
        self.u1.record_activity(self.at2)
        
        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 2)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 2)
        self.failUnlessEqual(action.users_completed, 0)
        
        self.u1.record_activity(self.at3)
        self.u2.record_activity(self.at2)
        
        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 3)
        self.failUnlessEqual(uap.is_completed, 1)
        uap = UserActionProgress.objects.get(user=self.u2, action=self.a)
        self.failUnlessEqual(uap.user_completes, 2)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 1)
        self.failUnlessEqual(action.users_completed, 1)
        
        self.u2.record_activity(self.at3)
        
        uap = UserActionProgress.objects.get(user=self.u2, action=self.a)
        self.failUnlessEqual(uap.user_completes, 3)
        self.failUnlessEqual(uap.is_completed, 1)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 0)
        self.failUnlessEqual(action.users_completed, 2)
        
    def test_total_points(self):    
        self.u1.record_activity(self.at1)
        
        user = User.objects.get(pk=self.u1.id)
        self.failUnlessEqual(user.get_profile().total_points, 5)
        
        self.u1.record_activity(self.at2)
        
        user = User.objects.get(pk=self.u1.id)
        self.failUnlessEqual(user.get_profile().total_points, 15)
        
        self.u1.record_activity(self.at3)
        
        user = User.objects.get(pk=self.u1.id)
        self.failUnlessEqual(user.get_profile().total_points, 35)
        
        self.u1.unrecord_activity(self.at2)
        
        user = User.objects.get(pk=self.u1.id)
        self.failUnlessEqual(user.get_profile().total_points, 25)
    
    def test_set_action_commitment(self):
        from datetime import date
        date_committed = date.today()
        self.u1.set_action_commitment(self.a, date_committed)
        
        uap = UserActionProgress.objects.filter(user=self.u1, action=self.a)
        self.failUnlessEqual(len(uap), 1)
        self.failUnlessEqual(uap[0].date_committed, date_committed)
    
    def test_get_action_progress(self):
        from datetime import date
        date_committed = date.today()
        UserActionProgress.objects.create(user=self.u1, action=self.a, date_committed=date_committed)
        
        progress = self.u1.get_action_progress(self.a)
        self.failUnlessEqual(progress.is_completed, 0)
        self.failUnlessEqual(progress.user_completes, 0)
        self.failUnlessEqual(progress.date_committed, date_committed)
        
        self.u1.record_activity(activity=self.at1)
        progress = self.u1.get_action_progress(self.a)
        self.failUnlessEqual(progress.is_completed, 0)
        self.failUnlessEqual(progress.user_completes, 1)
        
        self.u1.record_activity(activity=self.at2)
        self.u1.record_activity(activity=self.at3)
        progress = self.u1.get_action_progress(self.a)
        self.failUnlessEqual(progress.is_completed, 1)
        self.failUnlessEqual(progress.user_completes, 3)

    def test_get_commit_list(self):
        from datetime import date
        date_committed = date.today()
        self.u1.set_action_commitment(self.a, date_committed)
        
        commit_list = self.u1.get_commit_list()
        self.failUnlessEqual(len(commit_list), 1)
        
        commit_item = commit_list[0]
        self.failUnlessEqual(commit_item.action, self.a)
        self.failUnlessEqual(commit_item.date_committed, date_committed)

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
        
    def test_get_action_tasks_by_user(self):
        Record.objects.create(activity=self.at1, user=self.u1)
        Record.objects.create(activity=self.at3, user=self.u1)

        action_tasks = self.a.get_action_tasks_by_user(self.u1)

        self.failIfEqual(action_tasks[0].is_complete, None)
        self.failUnlessEqual(action_tasks[1].is_complete, None)
        self.failIfEqual(action_tasks[2].is_complete, None)
        
    def test_users_with_completes(self):
        """Also tests record_added and (part of) record_table_changed signals"""
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
        
    def test_actions_by_completion_status_with_user(self):
        actions, not_complete, in_progress, completed = Action.objects.actions_by_completion_status(self.u1)
        self.failUnlessEqual(len(actions), 1)
        self.failUnlessEqual(len(not_complete), 1)
        self.failIf(not_complete[0].actiontasks[0].completed)
        self.failIf(not_complete[0].actiontasks[1].completed)
        self.failIf(not_complete[0].actiontasks[2].completed)
        self.failUnlessEqual(len(in_progress), 0)
        self.failUnlessEqual(len(completed), 0)
        
        Record.objects.create(activity=self.at1, user=self.u1)
        
        actions, not_complete, in_progress, completed = Action.objects.actions_by_completion_status(self.u1)
        self.failUnlessEqual(len(actions), 1)
        self.failUnlessEqual(len(not_complete), 0)
        self.failUnlessEqual(len(in_progress), 1)
        self.failUnless(in_progress[0].actiontasks[0].completed)
        self.failIf(in_progress[0].actiontasks[1].completed)
        self.failIf(in_progress[0].actiontasks[2].completed)
        self.failUnlessEqual(len(completed), 0)
        
        Record.objects.create(activity=self.at2, user=self.u1)
        
        actions, not_complete, in_progress, completed = Action.objects.actions_by_completion_status(self.u1)
        self.failUnlessEqual(len(actions), 1)
        self.failUnlessEqual(len(not_complete), 0)
        self.failUnlessEqual(len(in_progress), 1)
        self.failUnless(in_progress[0].actiontasks[0].completed)
        self.failUnless(in_progress[0].actiontasks[1].completed)
        self.failIf(in_progress[0].actiontasks[2].completed)
        self.failUnlessEqual(len(completed), 0)
        
        Record.objects.create(activity=self.at3, user=self.u1)
        
        actions, not_complete, in_progress, completed = Action.objects.actions_by_completion_status(self.u1)
        self.failUnlessEqual(len(actions), 1)
        self.failUnlessEqual(len(not_complete), 0)
        self.failUnlessEqual(len(in_progress), 0)
        self.failUnlessEqual(len(completed), 1)
        self.failUnless(completed[0].actiontasks[0].completed)
        self.failUnless(completed[0].actiontasks[1].completed)
        self.failUnless(completed[0].actiontasks[2].completed)
        
    def test_actions_by_completion_status_with_anon_user(self):
        actions, not_complete, in_progress, completed = Action.objects.actions_by_completion_status(AnonymousUser())
        self.failUnlessEqual(len(actions), 1)
        self.failUnlessEqual(len(not_complete), 1)
        self.failUnlessEqual(len(in_progress), 0)
        self.failUnlessEqual(len(completed), 0)
        
        Record.objects.create(activity=self.at1, user=self.u1)
        
        actions, not_complete, in_progress, completed = Action.objects.actions_by_completion_status(AnonymousUser())
        self.failUnlessEqual(len(actions), 1)
        self.failUnlessEqual(len(not_complete), 1)
        self.failUnlessEqual(len(in_progress), 0)
        self.failUnlessEqual(len(completed), 0)

    def test_completes_for_user(self):
        self.failUnlessEqual(self.a.completes_for_user(self.u1), 0)
        
        Record.objects.create(activity=self.at1, user=self.u1)
        self.failUnlessEqual(self.a.completes_for_user(self.u1), 1)
        
        Record.objects.create(activity=self.at2, user=self.u1)
        self.failUnlessEqual(self.a.completes_for_user(self.u1), 2)

        # Completing the same action task twice should not advance progress 
        self.failUnlessRaises(Exception, Record.objects.create, activity=self.at1, user=self.u1)
        
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