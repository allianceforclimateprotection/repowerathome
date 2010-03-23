from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.core.urlresolvers import reverse
from django.db import models
from django.test import TestCase
from django.test.client import Client

from flagged.models import Flag

from models import Post

class FlagManagerTest(TestCase):
    fixtures = ["test_flags.json",]
    
    def setUp(self):
        self.post_content_type = ContentType.objects.get(app_label="flagged", model="post")
        self.first_post = Post.objects.get(pk=1)
        self.second_post = Post.objects.get(pk=2)
        self.third_post = Post.objects.get(pk=3)
        self.test_user = User.objects.get(username="test")
        self.example_user = User.objects.get(username="example")
        
    def test_has_user_flagged_object(self):
        self.failUnless(Flag.objects.has_user_flagged_object(self.post_content_type, self.first_post.pk, self.test_user))
        self.failUnless(Flag.objects.has_user_flagged_object(self.post_content_type, self.first_post.pk, self.example_user))
        self.failUnless(Flag.objects.has_user_flagged_object(self.post_content_type, self.second_post.pk, self.test_user))
        self.failUnless(not Flag.objects.has_user_flagged_object(self.post_content_type, self.second_post.pk, self.example_user))
        self.failUnless(Flag.objects.has_user_flagged_object(self.post_content_type, self.third_post.pk, self.test_user))
        self.failUnless(not Flag.objects.has_user_flagged_object(self.post_content_type, self.third_post.pk, self.example_user))
        
    def test_flag_content(self):
        self.failUnless(not Flag.objects.has_user_flagged_object(self.post_content_type, self.second_post.pk, self.example_user))
        Flag.objects.flag_content(self.post_content_type, self.second_post.pk, self.example_user)
        self.failUnless(Flag.objects.has_user_flagged_object(self.post_content_type, self.second_post.pk, self.example_user))
        
        self.failUnless(Flag.objects.has_user_flagged_object(self.post_content_type, self.first_post.pk, self.test_user))
        Flag.objects.flag_content(self.post_content_type, self.first_post.pk, self.test_user)
        self.failUnless(Flag.objects.has_user_flagged_object(self.post_content_type, self.first_post.pk, self.test_user))
        
    def test_unflag_content(self):
        self.failUnless(not Flag.objects.has_user_flagged_object(self.post_content_type, self.second_post.pk, self.example_user))
        Flag.objects.unflag_content(self.post_content_type, self.second_post.pk, self.example_user)
        self.failUnless(not Flag.objects.has_user_flagged_object(self.post_content_type, self.second_post.pk, self.example_user))
        
        self.failUnless(Flag.objects.has_user_flagged_object(self.post_content_type, self.first_post.pk, self.test_user))
        Flag.objects.unflag_content(self.post_content_type, self.first_post.pk, self.test_user)
        self.failUnless(not Flag.objects.has_user_flagged_object(self.post_content_type, self.first_post.pk, self.test_user))        
        
class FlagViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.post = Post.objects.create(content="test post")
        self.post_content_type = ContentType.objects.get(app_label="flagged", model="post")
        self.url = reverse("flagged-flag")
        
    def test_login_required(self):
        response = self.client.get(self.url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        
    def test_post_required(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.url, follow=True)
        self.failUnlessEqual(response.status_code, 405)
        
    def test_missing_parameter(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk}, follow=True)
        self.failUnlessEqual(response.status_code, 404)
        
    def test_invalid_parameters(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": "9876"}, follow=True)
        self.failUnlessEqual(response.status_code, 404)
        
    def test_success_with_next(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": self.post.pk, 
            "next": "/login/"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        
    def test_success(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": self.post.pk}, follow=True)
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["feedback@repowerathome.com"])
        self.failUnlessEqual(email.subject, "Content Flagged")
        self.failUnlessEqual(response.template[0].name, "flagged/email.html")
        self.failUnlessEqual(response.template[1].name, "flagged/flagged.html")
        self.failUnlessEqual(response.context["success"], True)
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        
    def test_success_ajax(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": self.post.pk}, 
            HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["feedback@repowerathome.com"])
        self.failUnlessEqual(email.subject, "Content Flagged")
        self.failUnlessEqual(response.template[0].name, "flagged/email.html")
        self.failUnlessEqual(response.template[1].name, "flagged/ajax/flagged.html")
        self.failUnlessEqual(response.context["success"], True)
        
    def test_already_created(self):
        self.client.login(username="test@test.com", password="test")
        Flag.objects.flag_content(self.post_content_type, self.post.pk, self.user)
        mail.outbox.pop()
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": self.post.pk}, follow=True)
        self.failUnlessEqual(mail.outbox, [])
        self.failUnlessEqual(response.template.name, "flagged/flagged.html")
        self.failUnlessEqual(response.context["success"], False)
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)