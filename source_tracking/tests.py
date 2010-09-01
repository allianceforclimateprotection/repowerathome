from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from models import UserSource

class SourceTrackingTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        
    def test_register_no_codes(self):
        response = self.client.post(reverse("register"), {"first_name": "test", 
            "email": "test@test.com", "password1": "testing", "password2": "testing",}, follow=True)
        self.failUnlessEqual(response.template[0].name, "rah/home_logged_in.html")
        sources = UserSource.objects.all()
        self.failUnlessEqual(sources.count(), 1)
        test_source = sources[0]
        self.failUnlessEqual(test_source.user.email, "test@test.com")
        self.failUnlessEqual(test_source.source, "direct")
        self.failUnlessEqual(test_source.subsource, "")
        self.failUnlessEqual(test_source.referrer, "")
        
    def test_facebook_code(self):
        self.client.get(reverse("index"), {"source": "facebook"}, HTTP_REFERER="http://www.facebook.com/")
        response = self.client.post(reverse("register"), {"first_name": "test", 
            "email": "test@test.com", "password1": "testing", "password2": "testing",}, follow=True)
        self.failUnlessEqual(response.template[0].name, "rah/home_logged_in.html")
        sources = UserSource.objects.all()
        self.failUnlessEqual(sources.count(), 1)
        test_source = sources[0]
        self.failUnlessEqual(test_source.user.email, "test@test.com")
        self.failUnlessEqual(test_source.source, "facebook")
        self.failUnlessEqual(test_source.subsource, "")
        self.failUnlessEqual(test_source.referrer, "http://www.facebook.com/")
        
    def test_google_add_code(self):
        self.client.get(reverse("index"), {"source": "google_ad", "subsource": "md_campaign"}, 
            HTTP_REFERER="http://www.google.com/")
        response = self.client.post(reverse("register"), {"first_name": "test", 
            "email": "test@test.com", "password1": "testing", "password2": "testing",}, follow=True)
        self.failUnlessEqual(response.template[0].name, "rah/home_logged_in.html")
        sources = UserSource.objects.all()
        self.failUnlessEqual(sources.count(), 1)
        test_source = sources[0]
        self.failUnlessEqual(test_source.user.email, "test@test.com")
        self.failUnlessEqual(test_source.source, "google_ad")
        self.failUnlessEqual(test_source.subsource, "md_campaign")
        self.failUnlessEqual(test_source.referrer, "http://www.google.com/")
    
    def test_browse_site_before_register(self):
        self.client.get(reverse("index"), {"source": "google_ad", "subsource": "md_campaign"}, 
            HTTP_REFERER="http://www.google.com/")
        self.client.get(reverse("action_show"))
        self.client.get(reverse("blog_index"))
        self.client.get(reverse("register"))
        response = self.client.post(reverse("register"), {"first_name": "test", 
            "email": "test@test.com", "password1": "testing", "password2": "testing",}, follow=True)
        self.failUnlessEqual(response.template[0].name, "rah/home_logged_in.html")
        sources = UserSource.objects.all()
        self.failUnlessEqual(sources.count(), 1)
        test_source = sources[0]
        self.failUnlessEqual(test_source.user.email, "test@test.com")
        self.failUnlessEqual(test_source.source, "google_ad")
        self.failUnlessEqual(test_source.subsource, "md_campaign")
        self.failUnlessEqual(test_source.referrer, "http://www.google.com/")
        
    def test_return_with_different_tracking(self):
        self.client.get(reverse("index"), {"source": "google_ad", "subsource": "md_campaign"}, 
            HTTP_REFERER="http://www.google.com/")
        self.client.get(reverse("action_show"))
        self.client.get(reverse("register"), {"source": "facebook"}, HTTP_REFERER="http://www.facebook.com/")
        response = self.client.post(reverse("register"), {"first_name": "test", 
            "email": "test@test.com", "password1": "testing", "password2": "testing",}, follow=True)
        self.failUnlessEqual(response.template[0].name, "rah/home_logged_in.html")
        sources = UserSource.objects.all()
        self.failUnlessEqual(sources.count(), 1)
        test_source = sources[0]
        self.failUnlessEqual(test_source.user.email, "test@test.com")
        self.failUnlessEqual(test_source.source, "facebook")
        self.failUnlessEqual(test_source.subsource, "")
        self.failUnlessEqual(test_source.referrer, "http://www.facebook.com/")
        