from django.test import TestCase
from django.contrib.auth.models import AnonymousUser

from rah.models import User, Profile
from actions.models import Action, UserActionProgress
from records.models import Activity, Record

def create_test_users_and_action_tasks(object):
    """
    create a base set of users and action tasks and assign all of these variables to the given instance
    """
    object.u1 = User.objects.create(username='1', email='test@test.com')
    object.u2 = User.objects.create(username='2', email='test@test.net')
    object.a = Action.objects.create(name='test action')
    object.act1 = Activity.objects.get(slug='action_commitment')

class ChartPoint(TestCase):
    def test_add_record(self):
        pass
    
    def get_date_as_milli_from_epoch(self):
        pass

class UserTest(TestCase):
    def setUp(self):
        create_test_users_and_action_tasks(self)
    
    def test_set_action_commitment(self):
        from datetime import date
        date_committed = date.today()
        self.u1.set_action_commitment(self.a, date_committed)
        
        uap = UserActionProgress.objects.filter(user=self.u1, action=self.a)
        self.failUnlessEqual(len(uap), 1)
        self.failUnlessEqual(uap[0].date_committed, date_committed)

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