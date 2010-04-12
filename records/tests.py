import datetime

from django.test import TestCase

from records.models import ChartPoint, Record, Activity
from actions.models import Action
from rah.models import User


def create_test_users_and_action_tasks(object):
    """
    create a base set of users and action tasks and assign all of these variables to the given instance
    """
    object.u1 = User.objects.create(username='1', email='test@test.com')
    object.u2 = User.objects.create(username='2', email='test@test.net')
    object.a = Action.objects.create(name='test action', slug='test-action')
    object.act1 = Activity.objects.get(slug='action_commitment')

class ChartPointTest(TestCase):
    fixtures = ["test_actions.json",]
    
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test", email="test@test.com")
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.ror = Action.objects.get(slug="replace-your-outdated-refrigerator")
        self.rec_1 = Record.objects.create_record(self.user, "action_complete", self.iwh)
        self.rec_2 = Record.objects.create_record(self.user, "action_complete", self.ror)
        self.rec_3 = Record.objects.create_record(self.user, "mag_tweet")
        self.chart_point = ChartPoint(datetime.date.today())
    
    def test_add_record(self):
        self.chart_point.add_record(self.rec_1)
        self.chart_point.add_record(self.rec_2)
        self.failUnlessEqual(self.chart_point.records, [self.rec_1, self.rec_2])
        self.failUnlessEqual(self.chart_point.points, 110)
        
        yestarday_point = ChartPoint(datetime.date.today()-datetime.timedelta(1))
        yestarday_point.add_record(self.rec_1)
        yestarday_point.add_record(self.rec_2)
        self.failUnlessEqual(yestarday_point.records, [])
        self.failUnlessEqual(yestarday_point.points, 110)
        
    def test_get_date_as_milli_from_epoch(self):
        jan_1_2010 = ChartPoint(datetime.date(2010, 1, 1))
        self.failUnlessEqual(jan_1_2010.get_date_as_milli_from_epoch(), 1262304000000)
        
class RecordTest(TestCase):
    fixtures = ["test_actions.json",]
    
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test", email="test@test.com")
        self.iwh = Action.objects.get(slug="insulate-water-heater")
        self.ror = Action.objects.get(slug="replace-your-outdated-refrigerator")
        self.rec_1 = Record.objects.create_record(self.user, "action_complete", self.iwh)
        self.rec_2 = Record.objects.create_record(self.user, "action_complete", self.ror)
        self.rec_3 = Record.objects.create_record(self.user, "mag_tweet")
        
    def test_filter_voided_records(self):
        Record.objects.void_record(self.user, "action_complete", self.iwh)
        self.failUnlessEqual(list(Record.objects.all()), [self.rec_3, self.rec_2])
        
    def test_user_records(self):
        new_user = User.objects.create_user(username="new_user", password="new", email="new_user@test.com")
        rec_4 = Record.objects.create_record(new_user, "action_complete", self.iwh)
        self.failUnlessEqual(list(Record.objects.user_records(new_user)), [rec_4])
        
        Record.objects.void_record(self.user, "action_complete", self.ror)
        self.failUnlessEqual(list(Record.objects.user_records(self.user)), [self.rec_3, self.rec_1])
        
    def test_last_active(self):
        self.failUnlessEqual(Record.objects.last_active(self.user), self.rec_3.created)
        
    def test_create_record(self):
        self.failUnlessEqual(self.rec_1.user, self.user)
        ac_activity = Activity.objects.get(slug="action_complete")
        self.failUnlessEqual(self.rec_1.activity, ac_activity)
        self.failUnlessEqual(self.rec_1.points,40)
        self.failUnlessEqual(self.rec_1.content_objects.all()[0].content_object, self.iwh)

    def test_create_record_with_activity(self):
        cmu_activity = Activity.objects.get(slug="comment_mark_useful")
        rec_4 = Record.objects.create_record(self.user, cmu_activity)

        self.failUnlessEqual(rec_4.user.email, "test@test.com")
        self.failUnlessEqual(rec_4.activity.slug, "comment_mark_useful")
        self.failUnlessEqual(rec_4.points, 5)
        self.failUnlessEqual(len(rec_4.content_objects.all()), 0)
        
        