from django.test import TestCase
from django.contrib.auth.models import User

from geo.models import Location
from rah.models import Profile, Action

from models import Group, GroupUsers, MembershipRequests

class GroupTest(TestCase):
    fixtures = ["test_geo_02804.json", "test_groups.json", "test_actions.json", "test_actiontasks.json",]
    
    def setUp(self):
        self.user = User.objects.create(username="1", email="test@test.com")
        self.yankees = Group.objects.get(name="yankees")
        self.sabres = Group.objects.get(name="sabres")
        self.ny = Group.objects.get(name="New York")
    
    def test_create_geo_group(self):
        profile = self.user.get_profile()
        profile.location = Location.objects.get(zipcode="02804")
        profile.save()
        ri, washington_county, ashaway = [g[1] for g in Group.objects.user_geo_group_tuple(self.user)]
        self.failUnlessEqual(ri.name, "Rhode Island")
        self.failUnlessEqual(ri.slug, "ri")
        self.failUnlessEqual(ri.location_type, "S")
        self.failUnlessEqual(ri.parent, None)
        
        self.failUnlessEqual(washington_county.name, "Washington County")
        self.failUnlessEqual(washington_county.slug, "ri-washington-county")
        self.failUnlessEqual(washington_county.location_type, "C")
        self.failUnlessEqual(washington_county.parent, ri)
        
        self.failUnlessEqual(ashaway.name, "Ashaway, Rhode Island")
        self.failUnlessEqual(ashaway.slug, "ri-washington-county-ashaway")
        self.failUnlessEqual(ashaway.location_type, "P")
        self.failUnlessEqual(ashaway.parent, washington_county)
        
    def test_is_joinable(self):
        self.failUnlessEqual(self.yankees.is_joinable(), True)
        self.failUnlessEqual(self.ny.is_joinable(), False)
        
    def test_is_public(self):
        self.failUnlessEqual(self.yankees.is_public(), True)
        self.failUnlessEqual(self.sabres.is_public(), False)
        self.failUnlessEqual(self.ny.is_public(), True)
        
    def test_is_member(self):
        self.failUnlessEqual(self.yankees.safe_image(), "images/yankees.jpg")
        self.failUnlessEqual(self.sabres.safe_image(), "images/theme/default_group.png")
        self.failUnlessEqual(self.ny.safe_image(), "images/theme/geo_group.jpg")
        
    def test_completed_actions_by_user(self):
        GroupUsers.objects.create(group=self.yankees, user=self.user)
        water_heater = Action.objects.get(name="Insulate your water heater")
        for task in water_heater.actiontask_set.all():
            task.complete_task(self.user)
        second_user = User.objects.create(username="2", email="test@example.com")
        GroupUsers.objects.create(group=self.yankees, user=second_user)
        fridge = Action.objects.get(name="Replace your outdated refrigerator")
        for task in fridge.actiontask_set.all():
            task.complete_task(self.user)
            task.complete_task(second_user)
 
        water_heater, fridge = self.yankees.completed_actions_by_user()
        self.failUnlessEqual(water_heater.users_completed, 2)
        self.failUnlessEqual(fridge.users_completed, 1)
        
        water_heater.actiontask_set.all()[0].complete_task(self.user, undo=True)
        water_heater, fridge = self.yankees.completed_actions_by_user()
        self.failUnlessEqual(water_heater.users_completed, 1)
        self.failUnlessEqual(fridge.users_completed, 1)
        
    def test_members_ordered_by_points(self):
        GroupUsers.objects.create(group=self.yankees, user=self.user)
        water_heater = Action.objects.get(name="Insulate your water heater")
        for task in water_heater.actiontask_set.all():
            task.complete_task(self.user)
        second_user = User.objects.create(username="2", email="test@example.com")
        GroupUsers.objects.create(group=self.yankees, user=second_user)
        fridge = Action.objects.get(name="Replace your outdated refrigerator")
        for task in fridge.actiontask_set.all():
            task.complete_task(self.user)
            task.complete_task(second_user)
   
        user, second_user = self.yankees.members_ordered_by_points()
        self.failUnlessEqual(user.get_profile().total_points, 55)
        self.failUnlessEqual(second_user.get_profile().total_points, 30)
        
        self.failUnlessEqual(user.actions_completed, 2)
        self.failUnlessEqual(second_user.actions_completed, 1)
        
    def test_group_records(self):
        GroupUsers.objects.create(group=self.yankees, user=self.user)
        water_heater = Action.objects.get(name="Insulate your water heater")
        for task in water_heater.actiontask_set.all():
            task.complete_task(self.user)
        second_user = User.objects.create(username="2", email="test@example.com")
        GroupUsers.objects.create(group=self.yankees, user=second_user)
        fridge = Action.objects.get(name="Replace your outdated refrigerator")
        for task in fridge.actiontask_set.all():
            task.complete_task(self.user)
            task.complete_task(second_user)
            
        records = self.yankees.group_records()
        self.failUnlessEqual(records.count(), 7)
        first = records[0]
        self.failUnlessEqual(first.user, second_user)
        last = records[6]
        self.failUnlessEqual(last.user, self.user)
        
    def test_has_pending_membership(self):
        self.failUnlessEqual(self.yankees.has_pending_membership(self.user), False)
        MembershipRequests.objects.create(group=self.yankees, user=self.user)
        self.failUnlessEqual(self.yankees.has_pending_membership(self.user), True)
        
    def test_requesters_to_grant_or_deny(self):
        self.failUnlessEqual(list(self.yankees.requesters_to_grant_or_deny(self.user)), [])
        GroupUsers.objects.create(group=self.yankees, user=self.user, is_manager=True)
        self.failUnlessEqual(list(self.yankees.requesters_to_grant_or_deny(self.user)), [])
        second_user = User.objects.create(username="2", email="test@example.com")
        MembershipRequests.objects.create(group=self.yankees, user=second_user)
        self.failUnlessEqual(list(self.yankees.requesters_to_grant_or_deny(self.user)), [second_user])
        
    def test_is_user_manager(self):
        GroupUsers.objects.create(group=self.yankees, user=self.user, is_manager=True)
        GroupUsers.objects.create(group=self.sabres, user=self.user)
        GroupUsers.objects.create(group=self.ny, user=self.user, is_manager=True)
        
        self.failUnlessEqual(self.yankees.is_user_manager(self.user), True)
        self.failUnlessEqual(self.sabres.is_user_manager(self.user), False)
        self.failUnlessEqual(self.ny.is_user_manager(self.user), False)
        
    def test_parents(self):
        profile = self.user.get_profile()
        profile.location = Location.objects.get(zipcode="02804")
        profile.save()
        ri, washington_county, ashaway = Group.objects.filter(users=self.user, is_geo_group=True)
        
        self.failUnlessEqual(ri.parents(), [])
        self.failUnlessEqual(washington_county.parents(), [ri])
        self.failUnlessEqual(ashaway.parents(), [ri, washington_county])