from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.test import TestCase
from django.test.client import Client

from rateable.models import Rating

from models import Post

class RatingManagerTest(TestCase):
    fixtures = ["test_ratings.json",]
    
    def setUp(self):
        self.post_content_type = ContentType.objects.get(app_label="rateable", model="post")
        self.first_post = Post.objects.get(pk=1)
        self.second_post = Post.objects.get(pk=2)
        self.third_post = Post.objects.get(pk=3)
        self.test_user = User.objects.get(username="test")
        self.example_user = User.objects.get(username="example")
        
    def test_get_users_score(self):
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.first_post, self.test_user), 1)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.first_post, self.example_user), 0)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.second_post, self.test_user), 1)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.second_post, self.example_user), 1)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.third_post, self.test_user), 1)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.third_post, self.example_user), None)
        
    def test_create_or_update(self):
        Rating.objects.create_or_update(self.post_content_type, self.third_post.pk, self.test_user, 2)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.third_post, self.test_user), 2)
        Rating.objects.create_or_update(self.post_content_type, self.third_post.pk, self.example_user, 3)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.third_post, self.example_user), 3)
        
class RateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.post = Post.objects.create(content="test post")
        self.post_content_type = ContentType.objects.get(app_label="rateable", model="post")
        self.url = reverse("rateable-rate")

    def test_login_required(self):
        response = self.client.get(self.url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")

    def test_post_required(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.url)
        self.failUnlessEqual(response.status_code, 405)
        
    def test_missing_parameter(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk})
        self.failUnlessEqual(response.status_code, 404)

    def test_invalid_parameters(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": "9876"})
        self.failUnlessEqual(response.status_code, 404)
        
    def test_missing_score(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": self.post.pk})
        self.failUnlessEqual(response.status_code, 404)
        
    def test_success_with_next(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": self.post.pk, 
            "score": "1", "next": "/login/"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post, self.user), 1)
        
    def test_successful_helpful(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": self.post.pk, "score": "1"})
        self.failUnlessEqual(response.template.name, "rateable/rated.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        self.failUnlessEqual(response.context["rating"].score, 1)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post, self.user), 1)        
        
    def test_successful_not_helpful(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": self.post.pk, "score": "0"})
        self.failUnlessEqual(response.template.name, "rateable/rated.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        self.failUnlessEqual(response.context["rating"].score, 0)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post, self.user), 0)
        
    def test_successful_helpful_ajax(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": self.post.pk, "score": "1"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.failUnlessEqual(response.template.name, "rateable/ajax/rated.json")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        self.failUnlessEqual(response.context["rating"].score, 1)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post, self.user), 1)
        
    def test_already_rated_changed(self):
        self.client.login(username="test@test.com", password="test")
        Rating.objects.create(content_type=self.post_content_type, object_pk=self.post.pk, user=self.user, score=2)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post, self.user), 2)
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": self.post.pk, "score": "1"})
        self.failUnlessEqual(response.template.name, "rateable/rated.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        self.failUnlessEqual(response.context["rating"].score, 1)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post, self.user), 1)
        
    def test_already_rated_not_changed(self):
        self.client.login(username="test@test.com", password="test")
        Rating.objects.create(content_type=self.post_content_type, object_pk=self.post.pk, user=self.user, score=0)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post, self.user), 0)
        response = self.client.post(self.url, {"content_type": self.post_content_type.pk, "object_pk": self.post.pk, "score": "0"})
        self.failUnlessEqual(response.template.name, "rateable/rated.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        self.failUnlessEqual(response.context["rating"].score, 0)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post, self.user), 0)