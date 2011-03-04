import re

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template import Context, Template
from django.test import TestCase
from django.test.client import Client

from utils import hash_val

from records.models import Record
from invite.models import Invitation, Rsvp, make_token

from models import Post

class MakeTokenTest(TestCase):
    def test_make_token(self):
        match = True if re.match(r'[a-f0-9]{15}', make_token()) else False
        self.failUnlessEqual(match, True)

class InviteTagTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.request = HttpRequest()
        self.request.user = user

    def test_invite_form(self):
        template = Template("{% load invites %}{% get_invite_form %}")
        html = template.render(Context({"request": self.request}))
        self.failUnless('<input type="hidden" name="content_type" id="id_content_type" />' in html)
        self.failUnless('<input type="hidden" name="object_pk" id="id_object_pk" />' in html)

    def test_invite_form_for_post(self):
        post = Post.objects.create(content="test post")
        post_content_type = ContentType.objects.get(app_label="invite", model="post")
        template = Template("{% load invites %}{% get_invite_form for post %}")
        html = template.render(Context({"request": self.request, "post": post}))
        self.failUnless('<input type="hidden" name="content_type" value="%s" id="id_content_type" />'
            % post_content_type.pk in html)
        self.failUnless('<input type="hidden" name="object_pk" value="%s" id="id_object_pk" />'
            % post.pk in html)

class InviteViewTest(TestCase):
    fixtures = ["invite.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.post = Post.objects.create(content="test post")
        self.post_content_type = ContentType.objects.get(app_label="invite", model="post")
        self.url = reverse("invite-invite")

    def test_login_required(self):
        response = self.client.get(self.url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")

    def test_post_required(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.url, follow=True)
        self.failUnlessEqual(response.status_code, 405)

    def test_missing_signature(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"emails": "invalid_email", "content_type": self.post_content_type.pk, 
            "object_pk": self.post.pk, "token": "81yuksdfkq2ro2i", 
            "next": "/login/"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("error" in message.tags)

    def test_invalid_signature(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"emails": "invalid_email", "content_type": self.post_content_type.pk, 
            "object_pk": self.post.pk, "signature": "fake_signature", "token": "81yuksdfkq2ro2i", 
            "next": "/login/"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("error" in message.tags)

    def test_invalid_email(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"emails": "invalid_email", "content_type": self.post_content_type.pk, 
            "object_pk": self.post.pk, "signature": hash_val((self.post_content_type, self.post.pk,)), 
            "token": "81yuksdfkq2ro2i", "next": "/login/"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("error" in message.tags)

    def test_valid_default_invite(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"emails": "bob@email.com", "content_type": "", 
            "object_pk": "", "signature": hash_val((self.post_content_type, self.post.pk,)), 
            "token": "81yuksdfkq2ro2i", "next": "/login/"}, follow=True)
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["bob@email.com"])
        self.failUnlessEqual(email.subject, "Invitation from %s to Repower at Home" % self.user.get_full_name())
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)

    def test_valid_post_invite(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"emails": "bob@email.com", "content_type": self.post_content_type.pk, 
            "object_pk": self.post.pk, "signature": hash_val((self.post_content_type, self.post.pk,)), 
            "token": "81yuksdfkq2ro2i", "next": "/login/"}, follow=True)
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["bob@email.com"])
        self.failUnlessEqual(email.subject, "Invitation from %s to Repower at Home" % self.user.get_full_name())
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)

    def test_vmultiple_emails(self):
         self.client.login(username="test@test.com", password="test")
         response = self.client.post(self.url, {"emails": "bob@email.com, george@email.com", "content_type": self.post_content_type.pk, 
             "object_pk": self.post.pk, "signature": hash_val((self.post_content_type, self.post.pk,)), 
             "token": "81yuksdfkq2ro2i", "next": "/login/"}, follow=True)
         email = mail.outbox.pop()
         self.failUnlessEqual(email.to, ["george@email.com"])
         self.failUnlessEqual(email.subject, "Invitation from %s to Repower at Home" % self.user.get_full_name())
         email = mail.outbox.pop()
         self.failUnlessEqual(email.to, ["bob@email.com"])
         self.failUnlessEqual(email.subject, "Invitation from %s to Repower at Home" % self.user.get_full_name())
         self.failUnlessEqual(response.template[0].name, "registration/login.html")
         message = iter(response.context["messages"]).next()
         self.failUnless("success" in message.tags)

class RsvpViewTest(TestCase):
    fixtures = ["actions.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.post = Post.objects.create(content="test post")
        self.post_content_type = ContentType.objects.get(app_label="invite", model="post")
        self.invite = Invitation.objects.create(user=self.user, email="bob@email.com", token=make_token())
        self.new_user = User.objects.create_user(username="2", email="new@test.com", password="new")

    def test_login_required(self):
        response = self.client.get(reverse("invite-rsvp", args=[self.invite.token]), follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")

    def test_invalid_token(self):
        self.client.login(username="new@test.com", password="new")
        response = self.client.get(reverse("invite-rsvp", args=["a5f02eb5710c41b"]), follow=True)
        self.failUnlessEqual(response.status_code, 404)

    def test_self_accepted_rsvp(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(reverse("invite-rsvp", args=[self.invite.token]), follow=True)
        self.failUnlessEqual(response.template[0].name, "rah/profile.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("info" in message.tags)
        records = Record.objects.user_records(user=self.user)
        self.failUnlessEqual(len(records), 0)

    def test_valid_rsvp(self):
        self.client.login(username="new@test.com", password="new")
        response = self.client.get(reverse("invite-rsvp", args=[self.invite.token]), follow=True)
        self.failUnlessEqual(response.template[0].name, "rah/profile.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        records = Record.objects.user_records(user=self.user)
        self.failUnlessEqual(len(records), 1)
        record = records[0]
        self.failUnlessEqual(record.user, self.user)
        self.failUnlessEqual(record.activity.slug, "mag_invite_friend")

    def test_used_rsvp(self):
        self.client.login(username="new@test.com", password="new")
        response = self.client.get(reverse("invite-rsvp", args=[self.invite.token]), follow=True)
        records = Record.objects.user_records(user=self.user)
        self.failUnlessEqual(len(records), 1)
        response = self.client.get(reverse("invite-rsvp", args=[self.invite.token]), follow=True)
        self.failUnlessEqual(response.template[0].name, "rah/profile.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("info" in message.tags)
        records = Record.objects.user_records(user=self.user)
        self.failUnlessEqual(len(records), 1)
