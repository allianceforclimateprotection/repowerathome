from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
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
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post_content_type, self.first_post.pk, self.test_user), 1)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post_content_type, self.first_post.pk, self.example_user), 0)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post_content_type, self.second_post.pk, self.test_user), 1)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post_content_type, self.second_post.pk, self.example_user), 1)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post_content_type, self.third_post.pk, self.test_user), 1)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post_content_type, self.third_post.pk, self.example_user), None)
        
    def test_create_or_update(self):
        Rating.objects.create_or_update(self.post_content_type, self.third_post.pk, self.test_user, 2)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post_content_type, self.third_post.pk, self.test_user), 2)
        Rating.objects.create_or_update(self.post_content_type, self.third_post.pk, self.example_user, 3)
        self.failUnlessEqual(Rating.objects.get_users_current_score(self.post_content_type, self.third_post.pk, self.example_user), 3)
        