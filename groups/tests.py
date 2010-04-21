import datetime
import re

from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.core import mail, management, files
from django.core.urlresolvers import reverse
from django.db import models
from django.test import TestCase
from django.test.client import Client

from geo.models import Location
from rah.models import Profile
from actions.models import Action

from models import Group, GroupUsers, MembershipRequests, DiscussionBlacklist, Discussion
        
class GroupDiscViews(TestCase):
    fixtures = ["test_groups.json"]
    
    def setUp(self):
        self.group_user = User.objects.create_user(username="gu", email="gu@test.com", password="gu")
        self.group_manager = User.objects.create_user(username="gm", email="gm@test.com", password="gm")
        self.group = Group.objects.get(slug="yankees")
        GroupUsers.objects.create(group=self.group, user=self.group_user)
        GroupUsers.objects.create(group=self.group, user=self.group_manager, is_manager=True)
        from utils import hash_val
        self.discs = {
            'd1': {"subject": "tc1 subject", "body": "tc1 body"},
            'd2': {"subject": "tc2 subject", "body": "tc2 body", "parent_id": 1, "parent_id_sig": hash_val(1)}
        }
        
        self.urls = {
            'group_disc_create': reverse("group_disc_create", kwargs={"group_slug": self.group.slug}),
            'group_disc_list': reverse("group_disc_list", kwargs={"group_slug": self.group.slug}),
            'd1': reverse("group_disc_detail", kwargs={"group_slug": self.group.slug, "disc_id": 1}),
            'd1_remove': reverse("group_disc_remove", kwargs={"group_slug": self.group.slug, "disc_id": 1}),
            'd1_approve': reverse("group_disc_approve", kwargs={"group_slug": self.group.slug, "disc_id": 1}),
            'd2': reverse("group_disc_detail", kwargs={"group_slug": self.group.slug, "disc_id": 2}),
            'd2_remove': reverse("group_disc_remove", kwargs={"group_slug": self.group.slug, "disc_id": 2}),
        }
    
    def test_create_discussion_get(self):
        # Anon users should get redirected to login
        response = self.client.get(self.urls['group_disc_create'], follow=True)
        self.assertRedirects(response, "/login/?next=%2Fyankees%2Fdiscussions%2Fcreate%2F")
        
        # As a group member
        self.client.login(username="gu", password="gu")
        response = self.client.get(self.urls['group_disc_create'])
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.template[0].name, "groups/group_disc_create.html")
        
        # As a group manager
        self.client.logout()
        self.client.login(username="gm", password="gm")
        response = self.client.get(self.urls['group_disc_create'])
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.template[0].name, "groups/group_disc_create.html")
        
    def test_create_discussion_post(self):
        # login an create a disc
        self.client.login(username="gu", password="gu")
        response = self.client.post(self.urls['group_disc_create'], self.discs['d1'], follow=True)
        self.assertRedirects(response, self.urls['d1'])
        
        # Make sure the disc saved to the database correctly
        disc = Discussion.objects.get(pk=1)
        self.failUnlessEqual(disc.subject, self.discs['d1']['subject'])
        self.failUnlessEqual(disc.body, self.discs['d1']['body'])
        self.failUnlessEqual(disc.is_public, True)
        self.failUnlessEqual(disc.is_removed, False)
        self.failUnlessEqual(disc.user, self.group_user)
        self.failUnlessEqual(disc.group, self.group)
        self.failUnlessEqual(disc.parent_id, None)
        
        # Check out the detail page
        response = self.client.get(self.urls['d1'])
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.template[0].name, "groups/group_disc_detail.html")
        
        # Check out the detail page
        response = self.client.get(self.urls['d1'])
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.template[0].name, "groups/group_disc_detail.html")
    
    def test_create_discussion_reply(self):
        self.client.login(username="gu", password="gu")
        self.client.post(self.urls['group_disc_create'], self.discs['d1'])
        self.client.logout()
        
        # Create a reply and make sure we're redirected back to the parent
        self.client.login(username="gm", password="gm")
        response = self.client.post(self.urls['group_disc_create'], self.discs['d2'], follow=True)
        self.assertRedirects(response, self.urls['d1'])
        
        disc = Discussion.objects.get(pk=2)
        self.failUnlessEqual(disc.subject, self.discs['d2']['subject'])
        self.failUnlessEqual(disc.body, self.discs['d2']['body'])
        self.failUnlessEqual(disc.is_public, True)
        self.failUnlessEqual(disc.is_removed, False)
        self.failUnlessEqual(disc.user, self.group_manager)
        self.failUnlessEqual(disc.group, self.group)
        self.failUnlessEqual(disc.parent_id, 1)
    
    def test_approve_comment(self):
        self.group.disc_moderation = 1
        self.group.save()
        
        self.client.login(username="gu", password="gu")
        self.client.post(self.urls['group_disc_create'], self.discs['d1'])
        
        # Make sure the comment is not public
        disc = Discussion.objects.get(pk=1)
        self.failUnlessEqual(disc.is_public, False)
        self.discs['d1']['is_public'] = disc.is_public
        
        # Try to approve comment as group member
        response = self.client.post(self.urls['d1_approve'], {'is_public': True})
        self.assertRedirects(response, self.urls['d1'])
        disc = Discussion.objects.get(pk=1)
        self.failUnlessEqual(disc.is_public, False)
        
        # Try to approve the comment as anon user
        self.client.logout()
        response = self.client.post(self.urls['d1_approve'], {'is_public': True})
        disc = Discussion.objects.get(pk=1)
        self.failUnlessEqual(disc.is_public, False)
        
        # Approve the comment as group manager
        self.client.login(username="gm", password="gm")
        response = self.client.post(self.urls['d1_approve'], {'is_public': True})
        self.assertRedirects(response, self.urls['d1'])
        disc = Discussion.objects.get(pk=1)
        self.failUnlessEqual(disc.is_public, True)
        
    def test_remove_comment(self):
        # Post a message as a group user
        self.client.login(username="gu", password="gu")
        self.client.post(self.urls['group_disc_create'], self.discs['d1'])
        self.client.post(self.urls['group_disc_create'], self.discs['d2'])
        
        # Make sure the comment posted
        d1 = Discussion.objects.get(pk=1)
        d2 = Discussion.objects.get(pk=1)
        self.failUnlessEqual(d1.is_removed, False)
        self.failUnlessEqual(d2.is_removed, False)
        
        # try to remove as group user
        response = self.client.post(self.urls['d1_remove'], {'is_removed': True})
        self.assertRedirects(response, self.urls['d1'])
        disc = Discussion.objects.get(pk=1)
        self.failUnlessEqual(disc.is_removed, False)
        
        # try to remove as an anon user
        self.client.logout()
        response = self.client.post(self.urls['d1_remove'], {'is_removed': True}, follow=True)
        self.assertRedirects(response, "/login/?next=%2Fgroups%2Fyankees%2Fdiscussions%2F1%2Fremove")
        disc = Discussion.objects.get(pk=1)
        self.failUnlessEqual(disc.is_removed, False)
        
        # remove as group manager
        self.client.login(username="gm", password="gm")
        response = self.client.post(self.urls['d1_remove'], {'is_removed': True})
        self.assertRedirects(response, self.urls['group_disc_list'])
        disc_count = Discussion.objects.filter(pk=1).count()
        self.failUnlessEqual(disc_count, 0)
        
    def test_only_manager_can_post(self):
        self.group.disc_post_perm = 1
        self.group.save()
        
        # Try to post as anon
        response = self.client.post(self.urls['group_disc_create'], self.discs['d1'])
        self.failUnlessEqual(response.status_code, 302)
        self.failUnlessEqual(Discussion.objects.all().count(), 0)
        
        # Try to post as a group user (not manager)
        self.client.login(username="gu", password="gu")
        response = self.client.post(self.urls['group_disc_create'], self.discs['d1'])
        self.failUnlessEqual(response.status_code, 403)
        self.failUnlessEqual(Discussion.objects.all().count(), 0)
        self.client.logout()
        
        # Try to post as a group manager
        self.client.login(username="gm", password="gm")
        response = self.client.post(self.urls['group_disc_create'], self.discs['d1'])
        self.assertRedirects(response, self.urls['d1'])
        self.failUnlessEqual(Discussion.objects.all().count(), 1)
        disc = Discussion.objects.get(pk=1)
        self.failUnlessEqual(disc.id, 1)
        
    def test_discussions_list(self):
        response = self.client.get(self.urls['group_disc_list'])
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.template[0].name, "groups/group_disc_list.html")
    
    def test_reply_count_signal(self):
        self.client.login(username="gm", password="gm")
        self.client.post(self.urls['group_disc_create'], self.discs['d1'])
        disc = Discussion.objects.get(pk=1)
        self.failUnlessEqual(disc.reply_count, 0)
        
        # Add a reply
        self.client.post(self.urls['group_disc_create'], self.discs['d2'])
        disc = Discussion.objects.get(pk=1)
        self.failUnlessEqual(disc.reply_count, 1)
        
        # Remove the reply
        response = self.client.post(self.urls['d2_remove'], {'is_removed': True})
        disc = Discussion.objects.get(pk=1)
        self.failUnlessEqual(disc.reply_count, 0)
    
    
class GroupTest(TestCase):
    fixtures = ["test_geo_02804.json", "test_groups.json", "test_actions.json",]
    
    def setUp(self):
        self.user = User.objects.create(username="1", email="test@test.com")
        self.yankees = Group.objects.get(name="yankees")
        self.sabres = Group.objects.get(name="sabres")
        self.ny = Group.objects.get(name="New York")
    
    def test_create_geo_group(self):
        profile = self.user.get_profile()
        profile.location = Location.objects.get(zipcode="02804")
        profile.save()
        ashaway, washington_county, ri = [g[1] for g in Group.objects.user_geo_group_tuple(self.user, 'P')]
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
        
    def test_create_dc_geo_group(self):
        management.call_command("loaddata", "test_geo_dc.json", verbosity=0)
        profile = self.user.get_profile()
        profile.location = Location.objects.get(zipcode="20001")
        profile.save()
        dc = Group.objects.user_geo_group_tuple(self.user, 'P')[0][1]
        self.failUnlessEqual(dc.name, "Washington, District Of Columbia")
        self.failUnlessEqual(dc.slug, "dc-district-of-columbia-washington")
        self.failUnlessEqual(dc.location_type, "P")
        self.failUnlessEqual(dc.parent, None)
        
    def test_set_geo_group_already_existing(self):
        management.call_command("loaddata", "test_geo_dc.json", verbosity=0)
        location = Location.objects.get(zipcode="20001")
        place = Group.objects.create_geo_group("P", location, None)
        profile = self.user.get_profile()
        profile.location = Location.objects.get(zipcode="20004")
        profile.save()
        dc = Group.objects.user_geo_group_tuple(self.user, 'P')[0][1]
        self.failUnlessEqual(dc.name, "Washington, District Of Columbia")
        self.failUnlessEqual(dc.slug, "dc-district-of-columbia-washington")
        self.failUnlessEqual(dc.location_type, "P")
        self.failUnlessEqual(dc.parent, None)
        
    def test_is_joinable(self):
        self.failUnlessEqual(self.yankees.is_joinable(), True)
        self.failUnlessEqual(self.ny.is_joinable(), False)
    
    def test_is_public(self):
        self.failUnlessEqual(self.yankees.is_public(), True)
        self.failUnlessEqual(self.sabres.is_public(), False)
        self.failUnlessEqual(self.ny.is_public(), True)
    
    def test_is_poster(self):
        # User who isn't a member of the group
        self.failUnlessEqual(self.sabres.is_poster(self.user), False)    
    
        # User who is a member of the group
        gu = GroupUsers.objects.create(group=self.sabres, user=self.user)
        self.failUnlessEqual(self.sabres.is_poster(self.user), True)
        
        # User is a member, but only managers can post
        self.sabres.disc_post_perm = 1
        self.sabres.save()
        self.failUnlessEqual(self.sabres.is_poster(self.user), False)
        
        # User is a manager
        gu.is_manager = True
        gu.save()
        self.failUnlessEqual(self.sabres.is_poster(self.user), True)
    
    def test_moderate_disc(self):
        # User who isn't a member of the group
        self.failUnlessEqual(self.sabres.moderate_disc(self.user), True)    
    
        # User who is a member of the group
        gu = GroupUsers.objects.create(group=self.sabres, user=self.user)
        self.failUnlessEqual(self.sabres.moderate_disc(self.user), False)
        
        # User is a member, but managers must moderate
        self.sabres.disc_moderation = 1
        self.sabres.save()
        self.failUnlessEqual(self.sabres.moderate_disc(self.user), True)
        
        # User is a manager
        gu.is_manager = True
        gu.save()
        self.failUnlessEqual(self.sabres.moderate_disc(self.user), False)
    
    # TODO: This test makes no sense!
    def test_is_member(self):
        self.failUnlessEqual(self.yankees.safe_image(), "images/yankees.jpg")
        self.failUnlessEqual(self.sabres.safe_image(), "images/theme/default_group.png")
        self.failUnlessEqual(self.ny.safe_image(), "images/theme/geo_group.jpg")
    
    def test_completed_actions_by_user(self):
        # GroupUsers.objects.create(group=self.yankees, user=self.user)
        # water_heater = Action.objects.get(name="Insulate your water heater")
        # for task in water_heater.actiontask_set.all():
        #     task.complete_task(self.user)
        # second_user = User.objects.create(username="2", email="test@example.com")
        # third_user = User.objects.create(username="3", email="test@example.net")
        # GroupUsers.objects.create(group=self.yankees, user=second_user)
        # fridge = Action.objects.get(name="Replace your outdated refrigerator")
        # for task in fridge.actiontask_set.all():
        #     task.complete_task(self.user)
        #     task.complete_task(second_user)
        #     task.complete_task(third_user)
        # 
        # fridge, water_heater = self.yankees.completed_actions_by_user()
        # self.failUnlessEqual(water_heater.completes_in_group, 1)
        # self.failUnlessEqual(fridge.completes_in_group, 2)
        # fridge.actiontask_set.all()[0].complete_task(self.user, undo=True)
        # actions = list(self.yankees.completed_actions_by_user())
        # self.failUnlessEqual(actions[0].completes_in_group, 1)
        # self.failUnlessEqual(actions[1].completes_in_group, 1)
        pass
    
    def test_members_ordered_by_points(self):
        # GroupUsers.objects.create(group=self.yankees, user=self.user)
        # water_heater = Action.objects.get(name="Insulate your water heater")
        # for task in water_heater.actiontask_set.all():
        #     task.complete_task(self.user)
        # second_user = User.objects.create(username="2", email="test@example.com")
        # third_user = User.objects.create(username="3", email="test@example.net")
        # GroupUsers.objects.create(group=self.yankees, user=second_user)
        # fridge = Action.objects.get(name="Replace your outdated refrigerator")
        # for task in fridge.actiontask_set.all():
        #     task.complete_task(self.user)
        #     task.complete_task(second_user)
        #     task.complete_task(third_user)
        # 
        # user, second_user = self.yankees.members_ordered_by_points()
        # self.failUnlessEqual(user.get_profile().total_points, 55)
        # self.failUnlessEqual(second_user.get_profile().total_points, 30)
        # 
        # self.failUnlessEqual(user.actions_completed, 2)
        # self.failUnlessEqual(second_user.actions_completed, 1)
        # TODO: rewrite after actions have been re facotred
        pass
    
    def test_group_records(self):
        user_2 = User.objects.create(username="2", email="test@test.edu")
        Profile.objects.filter(user=user_2).update(is_profile_private=True)
        user_3 = User.objects.create(username="3", email="test@test.net")
        
        GroupUsers.objects.create(group=self.yankees, user=self.user)
        GroupUsers.objects.create(group=self.yankees, user=user_2)
        GroupUsers.objects.create(group=self.yankees, user=user_3)
        
        iwh = Action.objects.get(slug="insulate-water-heater")
        ror = Action.objects.get(slug="replace-your-outdated-refrigerator")
        
        today = datetime.date.today()
        
        iwh.complete_for_user(self.user)
        iwh.commit_for_user(user_2, today)
        iwh.complete_for_user(user_3)
        
        ror.commit_for_user(self.user, today)
        ror.complete_for_user(user_2)
        ror.commit_for_user(user_3, today)
        
        iwh.undo_for_user(user_3)
        ror.cancel_for_user(user_2)
        
        records = self.yankees.group_records()
        self.failUnlessEqual(len(records), 3)
        
        ror_3, ror_1, iwh_1 = records
        self.failUnlessEqual(ror_3.user, user_3)
        self.failUnlessEqual(ror_3.content_objects.all()[0].content_object, ror)
        self.failUnlessEqual(ror_1.user, self.user)
        self.failUnlessEqual(ror_1.content_objects.all()[0].content_object, ror)
        self.failUnlessEqual(iwh_1.user, self.user)
        self.failUnlessEqual(iwh_1.content_objects.all()[0].content_object, iwh)
        
        records = self.yankees.group_records(2)
        self.failUnlessEqual(len(records), 2)
    
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
        
    def test_groups_not_blacklisted_by_user(self):
        groups = list(Group.objects.groups_not_blacklisted_by_user(self.user))
        self.failUnlessEqual(groups, [])
        
        GroupUsers.objects.create(group=self.yankees, user=self.user, is_manager=True)
        GroupUsers.objects.create(group=self.sabres, user=self.user)
        GroupUsers.objects.create(group=self.ny, user=self.user, is_manager=True)
        groups = list(Group.objects.groups_not_blacklisted_by_user(self.user))
        self.failUnlessEqual(groups, [self.yankees, self.sabres, self.ny])
        
        DiscussionBlacklist.objects.create(group=self.yankees, user=self.user)
        DiscussionBlacklist.objects.create(group=self.sabres, user=self.user)
        groups = list(Group.objects.groups_not_blacklisted_by_user(self.user))
        self.failUnlessEqual(groups, [self.ny])
        
        DiscussionBlacklist.objects.get(group=self.sabres, user=self.user).delete()
        groups = list(Group.objects.groups_not_blacklisted_by_user(self.user))
        self.failUnlessEqual(groups, [self.sabres, self.ny])
        
    def test_users_not_blacklisted(self):
        user_net = User.objects.create(username="2", email="test@test.net")
        user_edu = User.objects.create(username="3", email="test@test.edu")
        self.failUnlessEqual(list(self.yankees.users_not_blacklisted()), [])
        
        GroupUsers.objects.create(group=self.yankees, user=self.user, is_manager=True)
        GroupUsers.objects.create(group=self.yankees, user=user_net)
        GroupUsers.objects.create(group=self.yankees, user=user_edu)
        self.failUnlessEqual(list(self.yankees.users_not_blacklisted()), [self.user, user_net, user_edu])
        
        DiscussionBlacklist.objects.create(group=self.yankees, user=self.user)
        DiscussionBlacklist.objects.create(group=self.yankees, user=user_edu)
        self.failUnlessEqual(list(self.yankees.users_not_blacklisted()), [user_net])
        
        DiscussionBlacklist.objects.get(group=self.yankees, user=user_edu).delete()
        self.failUnlessEqual(list(self.yankees.users_not_blacklisted()), [user_net, user_edu])

class GroupCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.group_create_url = reverse("group_create")
    
    def test_login_required(self):
        response = self.client.get(self.group_create_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/register.html")
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.group_create_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "groups/group_create.html")
    
    def test_valid(self):
        self.client.login(username="test@test.com", password="test")
        image = files.File(open("static/images/theme/geo_group.jpg"))
        response = self.client.post(self.group_create_url, {"name": "Test Group", "slug": "test-group",
            "description": "This is a test group", "image": image, "membership_type": "O"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
        test_group = response.context["group"]
        self.failUnlessEqual(test_group.slug, "test-group")
        self.failUnlessEqual(test_group.description, "This is a test group")
        self.failUnlessEqual(test_group.membership_type, "O")
        self.failUnless(re.match("group_images/%s(_\d+)?\.jpeg" % test_group.pk, test_group.image.name))
        test_group.image.delete()
    
    def test_missing_required(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.group_create_url, follow=True)
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 4)
        self.failUnlessEqual("name" in errors, True)
        self.failUnlessEqual("slug" in errors, True)
        self.failUnlessEqual("description" in errors, True)
        self.failUnlessEqual("image" in errors, False)
        self.failUnlessEqual("membership_type" in errors, True)
    
    def test_invalid_slug(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.group_create_url, {"name": "Test Group", "slug": "test group",
            "description": "This is a test group", "membership_type": "O"}, follow=True)
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 1)
        self.failUnlessEqual("slug" in errors, True)
    
    def test_non_unique_slug(self):
        Group.objects.create(name="new group", slug="test-group")
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.group_create_url, {"name": "Test Group", "slug": "test-group",
            "description": "This is a test group", "membership_type": "O"}, follow=True)
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 1)
        self.failUnlessEqual("slug" in errors, True)


class GroupLeaveViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.group = Group.objects.create(name="test group", slug="test-group")
        self.group_leave_url = reverse("group_leave", args=[self.group.id])
    
    def test_login_required(self):
        response = self.client.get(self.group_leave_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/register.html")
    
    def test_invalid_group_id(self):
        self.client.login(username="test@test.com", password="test")
        max_id = Group.objects.aggregate(max=models.Max("id"))["max"]
        leave_url = reverse("group_leave", args=[max_id+1])
        response = self.client.get(leave_url, follow=True)
        self.failUnlessEqual(response.status_code, 404)
    
    def test_geo_group_id(self):
        self.client.login(username="test@test.com", password="test")
        geo_group = Group.objects.create(name="geo group", slug="geo-group", is_geo_group=True)
        leave_url = reverse("group_leave", args=[geo_group.id])
        response = self.client.get(leave_url)
        self.failUnlessEqual(response.status_code, 404)
    
    def test_not_a_member(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.group_leave_url, follow=True)
        message = iter(response.context["messages"]).next()
        self.failUnless("error" in message.tags)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
    
    def test_only_manager(self):
        self.client.login(username="test@test.com", password="test")
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=True)
        response = self.client.get(self.group_leave_url, follow=True)
        message = iter(response.context["messages"]).next()
        self.failUnless("error" in message.tags)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
    
    def successful_leave(self):
        self.client.login(username="test@test.com", password="test")
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=False)
        response = self.client.get(self.group_leave_url, follow=True)
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")

class GroupJoinViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.group = Group.objects.create(name="test group", slug="test-group")
        self.group_join_url = reverse("group_join", args=[self.group.id])
    
    def test_login_required(self):
        response = self.client.get(self.group_join_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/register.html")
    
    def test_invalid_group_id(self):
        self.client.login(username="test@test.com", password="test")
        max_id = Group.objects.aggregate(max=models.Max("id"))["max"]
        join_url = reverse("group_join", args=[max_id+1])
        response = self.client.get(join_url, follow=True)
        self.failUnlessEqual(response.status_code, 404)
    
    def test_geo_group_id(self):
        self.client.login(username="test@test.com", password="test")
        geo_group = Group.objects.create(name="geo group", slug="geo-group", is_geo_group=True)
        join_url = reverse("group_join", args=[geo_group.id])
        response = self.client.get(join_url)
        self.failUnlessEqual(response.status_code, 404)
    
    def test_already_a_member(self):
        self.client.login(username="test@test.com", password="test")
        GroupUsers.objects.create(user=self.user, group=self.group)
        response = self.client.get(self.group_join_url, follow=True)
        message = iter(response.context["messages"]).next()
        self.failUnless("error" in message.tags)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
    
    def test_membership_still_pending(self):
        self.client.login(username="test@test.com", password="test")
        MembershipRequests.objects.create(user=self.user, group=self.group)
        response = self.client.get(self.group_join_url, follow=True)
        message = iter(response.context["messages"]).next()
        self.failUnless("error" in message.tags)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
    
    def test_successfully_join_public_group(self):
        self.client.login(username="test@test.com", password="test")
        self.group.membership_type = "O"
        self.group.save()
        response = self.client.get(self.group_join_url, follow=True)
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
        self.failUnless(GroupUsers.objects.filter(user=self.user, group=self.group).exists())
    
    def test_successfully_request_private_group_join(self):
        self.client.login(username="test@test.com", password="test")
        self.group.membership_type = "C"
        self.group.save()
        manager = User.objects.create(username="manager", email="manager@test.com")
        GroupUsers.objects.create(user=manager, group=self.group, is_manager=True)
        response = self.client.get(self.group_join_url, follow=True)
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
        self.failUnless(MembershipRequests.objects.filter(user=self.user, group=self.group).exists())
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, [manager.email])
        self.failUnlessEqual(email.subject, "Group Join Request")

class GroupMembershipRequestViewTest(object):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.requester = User.objects.create_user(username="requester", email="requester@test.com", password="requester")
        self.group = Group.objects.create(name="test group", slug="test-group")
        self.url = reverse(self.url_name, args=[self.group.id, self.requester.id])
    
    def test_login_required(self):
        response = self.client.get(self.url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/register.html")
    
    def test_invalid_group_id(self):
        self.client.login(username="test@test.com", password="test")
        max_id = Group.objects.aggregate(max=models.Max("id"))["max"]
        approve_url = reverse(self.url_name, args=[max_id+1, self.requester.id])
        response = self.client.get(approve_url)
        self.failUnlessEqual(response.status_code, 404)
    
    def test_geo_group_id(self):
        self.client.login(username="test@test.com", password="test")
        geo_group = Group.objects.create(name="geo group", slug="geo-group", is_geo_group=True)
        approve_url = reverse(self.url_name, args=[geo_group.id, self.requester.id])
        response = self.client.get(approve_url)
        self.failUnlessEqual(response.status_code, 404)
    
    def test_invalid_user_id(self):
        self.client.login(username="test@test.com", password="test")
        max_id = User.objects.aggregate(max=models.Max("id"))["max"]
        approve_url = reverse(self.url_name, args=[self.group.id, max_id+1])
        response = self.client.get(approve_url)
        self.failUnlessEqual(response.status_code, 404)
    
    def test_not_a_manager(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.url, follow=True)
        self.failUnlessEqual(response.status_code, 403)
    
    def test_did_not_request(self):
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=True)
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.url, follow=True)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("error" in message.tags)

class GroupMembershipApproveViewTest(GroupMembershipRequestViewTest, TestCase):
    def __init__(self, *args, **kwargs):
        self.url_name = "group_approve"
        super(TestCase, self).__init__(*args, **kwargs)
    
    def test_successful_approve(self):
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=True)
        MembershipRequests.objects.create(user=self.requester, group=self.group)
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.url, follow=True)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        self.failUnlessEqual(MembershipRequests.objects.filter(user=self.requester, group=self.group).exists(), False)
        self.failUnlessEqual(GroupUsers.objects.filter(user=self.requester, group=self.group).exists(), True)
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, [self.requester.email])
        self.failUnlessEqual(email.subject, "Group Membership Response")
        self.failUnless("approved your access" in email.body)
        

class GroupMembershipDenyViewTest(GroupMembershipRequestViewTest, TestCase):
    def __init__(self, *args, **kwargs):
        self.url_name = "group_deny"
        super(TestCase, self).__init__(*args, **kwargs)
    
    def test_successful_deny(self):
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=True)
        MembershipRequests.objects.create(user=self.requester, group=self.group)
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.url, follow=True)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        self.failUnlessEqual(MembershipRequests.objects.filter(user=self.requester, group=self.group).exists(), False)
        self.failUnlessEqual(GroupUsers.objects.filter(user=self.requester, group=self.group).exists(), False)
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, [self.requester.email])
        self.failUnlessEqual(email.subject, "Group Membership Response")
        self.failUnless("turned down" in email.body)

class GroupDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_invalid_group_id(self):
        detail_url = reverse("group_detail", args=["does-not-exisit-group"])
        response = self.client.get(detail_url)
        self.failUnlessEqual(response.status_code, 404)
    
    def test_geo_group_id(self):
        geo_group = Group.objects.create(name="geo group", slug="geo-group", is_geo_group=True)
        detail_url = reverse("group_detail", args=[geo_group.slug])
        response = self.client.get(detail_url)
        self.failUnlessEqual(response.status_code, 404)
    
    def test_valid_detail(self):
        group = Group.objects.create(name="test group", slug="test-group")
        detail_url = reverse("group_detail", args=[group.slug])
        response = self.client.get(detail_url)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")

class GeoGroupViewTest(TestCase):
    fixtures = ["test_geo_02804.json"]
    
    def setUp(self):
        self.client = Client()
        self.asahway = Location.objects.get(zipcode="02804")
    
    def test_state_geo_group(self):
        group = Group.objects.create_geo_group("S", self.asahway, None)
        url = reverse("geo_group_state", args=["RI"])
        response = self.client.get(url)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
    
    def test_county_geo_group(self):
        group = Group.objects.create_geo_group("C", self.asahway, None)
        url = reverse("geo_group_county", args=["RI", "washington-county"])
        response = self.client.get(url)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
    
    def test_place_geo_group(self):
        group = Group.objects.create_geo_group("P", self.asahway, None)
        url = reverse("geo_group_place", args=["RI", "washington-county", "ashaway"])
        response = self.client.get(url)
        self.failUnlessEqual(response.template[0].name, "groups/group_detail.html")
    
    def test_geo_group_not_yet_created(self):
        url = reverse("geo_group_county", args=["NY", "erie-county"])
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 404)
    
    def test_invalid_geo_group(self):
        url = reverse("geo_group_place", args=["HQ", "nowhere-county", "imaginaryville"])
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 404)

class GroupListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("group_list")
    
    def test_listing(self):
        for i in xrange(10):
            Group.objects.create(name="%s" % i, slug="slug-%s" % i)
        response = self.client.get(self.url)
        self.failUnlessEqual(response.template[0].name, "groups/group_list.html")
        self.failUnlessEqual(len(response.context["new_groups"]), 5)

class GroupEditViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.group = Group.objects.create(name="test group", slug="test-group")
        self.url = reverse("group_edit", args=[self.group.slug])
    
    def test_login_required(self):
        response = self.client.get(self.url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/register.html")
    
    def test_not_a_manager(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.url, follow=True)
        self.failUnlessEqual(response.status_code, 403)
    
    def test_valid_viewing(self):
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=True)
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.url)
        self.failUnlessEqual(response.template[0].name, "groups/group_edit.html")
    
    def test_missing_action_form(self):
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=True)
        self.client.login(username="test@test.com", password="test")
        image = open("static/images/theme/geo_group.jpg")
        response = self.client.post(self.url, {"name": "Test Group", "slug": "test-group",
            "description": "This is a test group", "image": image, "membership_type": "O"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "groups/group_edit.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("error" in message.tags)
        
    def test_invalid_change_group(self):
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=True)
        self.client.login(username="test@test.com", password="test")
        image = open("static/images/theme/geo_group.jpg")
        response = self.client.post(self.url, {"name": "Test Group", "slug": "test-group",
            "description": "This is a test group", "image": image, "change_group": "True"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "groups/group_edit.html")
        errors = response.context["group_form"].errors
        self.failUnless("membership_type" in errors)
        
    def test_valid_change_group(self):
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=True)
        self.client.login(username="test@test.com", password="test")
        image = open("static/images/theme/geo_group.jpg")
        response = self.client.post(self.url, {"name": "Changed Group", "slug": "changed-group",
            "description": "This is a test group", "image": image, "membership_type": "C", "change_group": "True"}, follow=True)
        test_group = response.context["group"]
        self.failUnlessEqual(response.template[0].name, "groups/group_edit.html")
        changed_group = Group.objects.get(pk=self.group.id)
        self.failUnlessEqual(changed_group.name, "Changed Group")
        test_group.image.delete()
        
    def test_delete_group(self):
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=True)
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"delete_group": "True"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "groups/group_list.html")
        self.failUnless(not Group.objects.filter(pk=self.group.pk).exists())

    def test_discussion_settings(self):
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=True)
        self.client.login(username="test@test.com", password="test")
        self.failUnlessEqual(self.group.disc_moderation, 0)
        self.failUnlessEqual(self.group.disc_post_perm, 0)
        response = self.client.post(self.url, {"disc_moderation": 1, "disc_post_perm": 1, "discussion_settings": 1}, follow=True)
        self.failUnlessEqual(response.template[0].name, "groups/group_edit.html")
        group = Group.objects.get(pk=self.group.pk)
        self.failUnlessEqual(group.disc_moderation, 1)
        self.failUnlessEqual(group.disc_post_perm, 1)
        
    def test_invalid_change_membership(self):
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=True)
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"role": "N", "memberships": "%s" % self.user.pk, 
            "change_membership": "True"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "groups/group_edit.html")
        errors = response.context["membership_form"].errors
        self.failUnless("memberships" in errors)
        
    def test_valid_change_membership(self):
        GroupUsers.objects.create(user=self.user, group=self.group, is_manager=True)
        new_user = User.objects.create(username="2", email="newuser@email.com")
        GroupUsers.objects.create(user=new_user, group=self.group, is_manager=False)
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"role": "M", "memberships": "%s" % new_user.pk, 
            "change_membership": "True"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "groups/group_edit.html")
        errors = response.context["membership_form"].errors
        self.failUnlessEqual(errors, {})
        self.failUnless(self.group.is_user_manager(new_user))
    
    
class BaseballViews(TestCase):
    fixtures = ["test_groups.json"]

    def setUp(self):
        self.group = Group.objects.get(slug="yankees")

    def test_does_team_suck(self):
        self.failUnlessEqual(self.group.name, "yankees")