from django.test import TestCase
from django.contrib.auth.models import AnonymousUser

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

class ChartPoint(TestCase):
    def test_add_record(self):
        pass
    
    def get_date_as_milli_from_epoch(self):
        pass

class UserTest(TestCase):
    def setUp(self):
        create_test_users_and_action_tasks(self)
        
    def test_record_action_task(self):        
        self.at1.complete_task(self.u1)
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
        
        self.at1.complete_task(self.u1)
        
        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 1)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 1)
        self.failUnlessEqual(action.users_completed, 0)
        
        self.at2.complete_task(self.u1)
        
        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 2)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 1)
        self.failUnlessEqual(action.users_completed, 0)
        
        self.at3.complete_task(self.u1)
        
        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 3)
        self.failUnlessEqual(uap.is_completed, 1)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 0)
        self.failUnlessEqual(action.users_completed, 1)
        
    def test_multi_user_complete_action(self):        
        self.at1.complete_task(self.u1)
        
        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 1)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 1)
        self.failUnlessEqual(action.users_completed, 0)
        
        self.at1.complete_task(self.u2)
        
        uap = UserActionProgress.objects.get(user=self.u2, action=self.a)
        self.failUnlessEqual(uap.user_completes, 1)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 2)
        self.failUnlessEqual(action.users_completed, 0)
        
        self.at2.complete_task(self.u1)
        
        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 2)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 2)
        self.failUnlessEqual(action.users_completed, 0)
        
        self.at3.complete_task(self.u1)
        self.at2.complete_task(self.u2)
        
        uap = UserActionProgress.objects.get(user=self.u1, action=self.a)
        self.failUnlessEqual(uap.user_completes, 3)
        self.failUnlessEqual(uap.is_completed, 1)
        uap = UserActionProgress.objects.get(user=self.u2, action=self.a)
        self.failUnlessEqual(uap.user_completes, 2)
        self.failUnlessEqual(uap.is_completed, 0)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 1)
        self.failUnlessEqual(action.users_completed, 1)
        
        self.at3.complete_task(self.u2)
        
        uap = UserActionProgress.objects.get(user=self.u2, action=self.a)
        self.failUnlessEqual(uap.user_completes, 3)
        self.failUnlessEqual(uap.is_completed, 1)
        action = Action.objects.get(pk=self.a.id)
        self.failUnlessEqual(action.users_in_progress, 0)
        self.failUnlessEqual(action.users_completed, 2)
    
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
        
        self.at1.complete_task(self.u1)
        progress = self.u1.get_action_progress(self.a)
        self.failUnlessEqual(progress.is_completed, 0)
        self.failUnlessEqual(progress.user_completes, 1)
        
        self.at2.complete_task(self.u1)
        self.at3.complete_task(self.u1)
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
        self.at1.complete_task(self.u1)
        
        action = Action.objects.actions_by_completion_status(self.u1)[0][0]
        
        self.failUnlessEqual(action.total_tasks, 3)
        self.failUnlessEqual(action.user_completes, 1)
    
    def test_partial_users_completes(self):
        self.at1.complete_task(self.u1)
        self.at2.complete_task(self.u2)
        self.at3.complete_task(self.u1)

        action1 = Action.objects.actions_by_completion_status(self.u1)[0][0]
        action2 = Action.objects.actions_by_completion_status(self.u2)[0][0]

        self.failUnlessEqual(action1.total_tasks, 3)
        self.failUnlessEqual(action1.user_completes, 2)
        self.failUnlessEqual(action2.total_tasks, 3)
        self.failUnlessEqual(action2.user_completes, 1)
        
    def test_all_users_completes(self):
        self.at1.complete_task(self.u1)
        self.at2.complete_task(self.u1)
        self.at3.complete_task(self.u1)
        self.at1.complete_task(self.u2)
        self.at2.complete_task(self.u2)
        self.at3.complete_task(self.u2)

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
        self.at1.complete_task(self.u1)
        self.at3.complete_task(self.u1)
        
        action_tasks = self.a.get_action_tasks_by_user(self.u1)

        self.failIfEqual(action_tasks[0].is_complete, None)
        self.failUnlessEqual(action_tasks[1].is_complete, None)
        self.failIfEqual(action_tasks[2].is_complete, None)
        
    def test_users_with_completes(self):
        """Also tests record_added and (part of) record_table_changed signals"""
        self.failUnlessEqual(self.a.users_with_completes()[0], 0)
        self.failUnlessEqual(self.a.users_with_completes()[2], 0)

        self.at1.complete_task(self.u1)
        action = Action.objects.get(id=self.a.id)
        self.failUnlessEqual(action.users_with_completes()[0], 1)
        self.failUnlessEqual(action.users_with_completes()[2], 0)

        self.at2.complete_task(self.u1)
        self.at1.complete_task(self.u2)
        action = Action.objects.get(id=self.a.id)
        self.failUnlessEqual(action.users_with_completes()[0], 2)
        self.failUnlessEqual(action.users_with_completes()[2], 0)

        self.at3.complete_task(self.u1)
        self.at2.complete_task(self.u2)
        action = Action.objects.get(id=self.a.id)
        self.failUnlessEqual(action.users_with_completes()[0], 1)
        self.failUnlessEqual(action.users_with_completes()[2], 1)

        self.at3.complete_task(self.u2)
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
        
        self.at1.complete_task(self.u1)
        
        actions, not_complete, in_progress, completed = Action.objects.actions_by_completion_status(self.u1)
        self.failUnlessEqual(len(actions), 1)
        self.failUnlessEqual(len(not_complete), 0)
        self.failUnlessEqual(len(in_progress), 1)
        self.failUnless(in_progress[0].actiontasks[0].completed)
        self.failIf(in_progress[0].actiontasks[1].completed)
        self.failIf(in_progress[0].actiontasks[2].completed)
        self.failUnlessEqual(len(completed), 0)
        
        self.at2.complete_task(self.u1)
        
        actions, not_complete, in_progress, completed = Action.objects.actions_by_completion_status(self.u1)
        self.failUnlessEqual(len(actions), 1)
        self.failUnlessEqual(len(not_complete), 0)
        self.failUnlessEqual(len(in_progress), 1)
        self.failUnless(in_progress[0].actiontasks[0].completed)
        self.failUnless(in_progress[0].actiontasks[1].completed)
        self.failIf(in_progress[0].actiontasks[2].completed)
        self.failUnlessEqual(len(completed), 0)
        
        self.at3.complete_task(self.u1)
        
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
        
        self.at1.complete_task(self.u1)
        
        actions, not_complete, in_progress, completed = Action.objects.actions_by_completion_status(AnonymousUser())
        self.failUnlessEqual(len(actions), 1)
        self.failUnlessEqual(len(not_complete), 1)
        self.failUnlessEqual(len(in_progress), 0)
        self.failUnlessEqual(len(completed), 0)

    def test_completes_for_user(self):
        self.failUnlessEqual(self.a.completes_for_user(self.u1), 0)
        
        self.at1.complete_task(self.u1)
        self.failUnlessEqual(self.a.completes_for_user(self.u1), 1)
        
        self.at3.complete_task(self.u1)
        self.failUnlessEqual(self.a.completes_for_user(self.u1), 2)

        # Failing on exception is not working, so this try/except/else is a workaround
        try:
            self.at1.complete_task(self.u1)
        except Exception, e:
            pass
        else:
            self.fail("Completing the same action task twice should have thrown an exception")
        
        # Completing the same action task twice should not advance progress
        self.failUnlessEqual(self.a.completes_for_user(self.u1), 2)
        
        
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