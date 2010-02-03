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
        # create_test_users_and_action_tasks(self)
        pass

    def test_get_name(self):
        u1 = User(username='1', email='test@test.com')
        u2 = User(username='2', email='test@test.net', first_name='first')
        u3 = User(username='3', email='test@test.org', last_name='last')
        u4 = User(username='4', email='test@test.edu', first_name='first', last_name='last')
        self.failUnlessEqual(u1.get_name(), 'test@test.com')
        self.failUnlessEqual(u2.get_name(), 'first')
        self.failUnlessEqual(u3.get_name(), 'last')
        self.failUnlessEqual(u4.get_name(), 'first last')
    
    def test_get_chart_data(self):
        pass
        # create_test_users_and_action_tasks(self)
        # Record(user=self.u1, activity=self.at1, points=self.at1.points).save()
        # Record(user=self.u1, activity=self.at2, points=self.at2.points).save()
        # Record(user=self.u1, activity=self.at3, points=self.at3.points).save()
        # 
        # chart_points = self.u1.get_chart_data()
        # point_data = [(chart_point.get_date_as_milli_from_epoch(), chart_point.points) for chart_point in chart_points]
        # problem here is that points aren't being collapsed
        # print chart_points[0].points
        # print Record.objects.all()[0].points
        # 
        # self.failUnlessEqual(len(chart_data), 3)
        # print Record.objects.all()[0].points
        # self.failUnlessEqual(chart_data[], 3)
        # print self.u1.get_chart_data()
    
    def test_get_latest_records(self):
        create_test_users_and_action_tasks(self)
        
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
        create_test_users_and_action_tasks(self)
        
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
        create_test_users_and_action_tasks(self)
        
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
        create_test_users_and_action_tasks(self)
        
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
        create_test_users_and_action_tasks(self)
        
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
        create_test_users_and_action_tasks(self)
        
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
        create_test_users_and_action_tasks(self)
        
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