from django.test import TestCase

from models import Event, Guest

class GuestTest(TestCase):
    fixtures = ["test_events.json",]
    
    def setUp(self):
        self.jane = Guest.objects.get(name="Jane Doe")
        self.alex = Guest.objects.get(name="Alex Smith")
        self.jon = Guest.objects.get(name="Jon Doe")
        self.me = Guest.objects.get(email="me@gmail.com")
        self.jonathan = Guest.objects.get(name="Jonathan")
        self.mike = Guest.objects.get(name="Mike Roberts")
        
    def test_status(self):
        self.failUnlessEqual(self.jane.status(), "Attending")
        self.failUnlessEqual(self.alex.status(), "Not Attending")
        self.failUnlessEqual(self.jon.status(), "Invited May 18")
        self.failUnlessEqual(self.me.status(), "Invited Mar 12")
        self.failUnlessEqual(self.jonathan.status(), "Added Feb 2")
        self.failUnlessEqual(self.mike.status(), "Maybe Attending")