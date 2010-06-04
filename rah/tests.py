from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser

from records.models import Activity, Record
from actions.models import Action, UserActionProgress

from models import Profile

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

class ProfileTest(TestCase):
    def setUp(self):
        test_user_email    = "test@test.com"
        user               = User(username='1', id=1, email=test_user_email)
        self.profile       = Profile.objects.create(user=user)
        self.expected_url  = "http://www.gravatar.com/avatar/b642b4217b34b1e8d3bd915fc65c4452?r=g&d=identicon&s=52"
        self.expected_hash = "b642b4217b34b1e8d3bd915fc65c4452"
        
    def test_get_gravatar_url(self):
        url = self.profile.get_gravatar_url()
        self.failUnlessEqual(url, self.expected_url)
    
    def test_email_hash(self):
        email_hash = self.profile._email_hash()
        self.failUnlessEqual(email_hash, self.expected_hash)