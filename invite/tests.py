import re

from django.test import TestCase
from invite.models import Invitation, Rsvp
from django.contrib.auth.models import User

class InviteModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", email="user@test.com", password="user")
        self.invitee = User.objects.create_user(username="invitee", email="invitee@test.com", password="invitee")
        self.invite = Invitation.objects.create(user=self.user, email=self.invitee.email, invite_type="some_type")
        
    def test_invite(self):
        self.failUnlessEqual(Invitation.objects.all().count(), 1)
        Invitation.objects.invite(self.user, "invitee@test.com", "some_type")
        Invitation.objects.invite(self.user, "invitee@test.com", "some_type", 1)
        self.failUnlessEqual(Invitation.objects.all().count(), 3)
    
    def test_rsvp(self):
        Invitation.objects.rsvp(self.invitee, self.invite)
        self.failUnlessEqual(Rsvp.objects.all().count(), 1)

    def test_make_token(self):
        token = Invitation.objects.make_token()
        match = True if re.match(r'[a-f0-9]{15}', token) else False
        self.failUnlessEqual(match, True)
    
class InviteViews(TestCase):
    def setUp(self):
        pass
    