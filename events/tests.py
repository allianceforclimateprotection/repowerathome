import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from geo.models import Location

from models import EventType, Event, Guest

class EventTest(TestCase):
    fixtures = ["test_geo_02804.json", "test_events.json",]
    
    def setUp(self):
        self.creator = User.objects.get(username="eric")
        self.event_type = EventType.objects.get(name="Energy Meeting")
        self.ashaway = Location.objects.get(zipcode="02804")
        self.event = Event.objects.get(pk=1)
            
    def test_has_manager_privileges(self):
        self.failUnlessEqual(self.event.has_manager_privileges(self.creator), True)
        hacker = User.objects.create_user(username="hacker", email="hacker@email.com", password="hacker")
        self.failUnlessEqual(self.event.has_manager_privileges(hacker), False)
        guest = Guest.objects.get(name="Jane Doe")
        guest.user = hacker
        guest.save()
        self.failUnlessEqual(self.event.has_manager_privileges(hacker), False)
        guest.is_host = True
        guest.save()
        self.failUnlessEqual(self.event.has_manager_privileges(hacker), True)
        
    def test_confirmed_guests(self):
        self.failUnlessEqual(self.event.confirmed_guests(), 1)
        alex = Guest.objects.get(name="Alex Smith")
        alex.rsvp_status = "A"
        alex.save()
        self.failUnlessEqual(self.event.confirmed_guests(), 2)
        jane = Guest.objects.get(name="Jane Doe")
        jane.rsvp_status = "N"
        jane.save()
        self.failUnlessEqual(self.event.confirmed_guests(), 1)
        
    def test_outstanding_invitations(self):
        self.failUnlessEqual(self.event.outstanding_invitations(), 2)
        jon = Guest.objects.get(name="Jon Doe")
        jon.rsvp_status = "M"
        jon.save()
        self.failUnlessEqual(self.event.outstanding_invitations(), 1)
        
    def test_place(self):
        self.failUnlessEqual(self.event.place(), "123 Garden Street Ashaway, RI")

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
        
class EventCreateViewTest(TestCase):
    fixtures = ["test_geo_02804.json"]
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.event_type = EventType.objects.create(name="Energy Meeting")
        self.event_create_url = reverse("event-create")
    
    def test_login_required(self):
        response = self.client.get(self.event_create_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        
    def test_get(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.event_create_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/create.html")
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 0)
    
    def test_missing_required(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": "", "where": "",
            "city": "", "state": "", "zipcode": "", "when": "", 
            "start": "", "end": "", "details": "", "is_private": "False"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/create.html")
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 7)
        self.failUnless("event_type" in errors)
        self.failUnless("where" in errors)
        self.failUnless("when" in errors)
        self.failUnless("start" in errors)
        self.failUnless("end" in errors)
        self.failUnless("details" in errors)
        
    def test_invalid_zipcode(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "", "state": "", "zipcode": "99999", "when": "2050-09-09", 
            "start": "10:00", "end": "11:00", "details": "test", "is_private": "False"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/create.html")
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 1)
        self.failUnless("zipcode" in errors)
        
    def test_invalid_when(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "", "state": "", "zipcode": "02804", "when": "2009-09-09", 
            "start": "10:00", "end": "11:00", "details": "test", "is_private": "False"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/create.html")
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 1)
        self.failUnless("when" in errors)
        
    def test_invalid_city_state(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "ashawa", "state": "RI", "zipcode": "", "when": "2050-09-09", 
            "start": "10:00", "end": "11:00", "details": "test", "is_private": "False"}, follow=True)
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 1)
        error = errors["__all__"][0]
        self.failUnless("place" in error)
        
    def test_missing_city_state_and_zipcode(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "", "state": "", "zipcode": "", "when": "2050-09-09", 
            "start": "10:00", "end": "11:00", "details": "test", "is_private": "False"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/create.html")
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 1)
        error = errors["__all__"][0]
        self.failUnless("city" in error)
        self.failUnless("state" in error)
        self.failUnless("zipcode" in error)
        
    def test_valid_city_state_create(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "ashaway", "state": "RI", "zipcode": "", "when": "2050-09-09", 
            "start": "10:00", "end": "11:00", "details": "test", "is_private": "False"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/show.html")
        event = response.context["event"]
        self.failUnlessEqual(event.event_type, self.event_type)
        self.failUnlessEqual(event.where, "11 Fake St.")
        self.failUnlessEqual(event.location.name, "Ashaway")
        self.failUnlessEqual(event.location.st, "RI")
        self.failUnlessEqual(event.location.zipcode, "02804")
        self.failUnlessEqual(event.when, datetime.date(2050, 9, 9))
        self.failUnlessEqual(event.start, datetime.time(10, 0))
        self.failUnlessEqual(event.end, datetime.time(11, 0))
        self.failUnlessEqual(event.details, "test")
        self.failUnlessEqual(event.is_private, False)
        
    def test_valid_zipcode_create(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "", "state": "", "zipcode": "02804", "when": "2050-09-09", 
            "start": "10:00", "end": "11:00", "details": "test", "is_private": "True"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/show.html")
        event = response.context["event"]
        self.failUnlessEqual(event.event_type, self.event_type)
        self.failUnlessEqual(event.where, "11 Fake St.")
        self.failUnlessEqual(event.location.name, "Ashaway")
        self.failUnlessEqual(event.location.st, "RI")
        self.failUnlessEqual(event.location.zipcode, "02804")
        self.failUnlessEqual(event.when, datetime.date(2050, 9, 9))
        self.failUnlessEqual(event.start, datetime.time(10, 0))
        self.failUnlessEqual(event.end, datetime.time(11, 0))
        self.failUnlessEqual(event.details, "test")
        self.failUnlessEqual(event.is_private, True)
        
    def test_valid_city_state_zipcode_create(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "ashaway", "state": "RI", "zipcode": "02804", "when": "2050-09-09", 
            "start": "10:00", "end": "11:00", "details": "test", "is_private": "True"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/show.html")
        event = response.context["event"]
        self.failUnlessEqual(event.event_type, self.event_type)
        self.failUnlessEqual(event.where, "11 Fake St.")
        self.failUnlessEqual(event.location.name, "Ashaway")
        self.failUnlessEqual(event.location.st, "RI")
        self.failUnlessEqual(event.location.zipcode, "02804")
        self.failUnlessEqual(event.when, datetime.date(2050, 9, 9))
        self.failUnlessEqual(event.start, datetime.time(10, 0))
        self.failUnlessEqual(event.end, datetime.time(11, 0))
        self.failUnlessEqual(event.details, "test")
        self.failUnlessEqual(event.is_private, True)
        
class EventEditViewTest(TestCase):
        fixtures = ["test_geo_02804.json", "test_events.json"]

        def setUp(self):
            self.client = Client()
            self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
            self.event_type = EventType.objects.get(pk=1)
            self.event = Event.objects.get(pk=1)
            self.event_edit_url = reverse("event-edit", args=[self.event.id])
            
        def test_login_required(self):
            response = self.client.get(self.event_edit_url, follow=True)
            self.failUnlessEqual(response.template[0].name, "registration/login.html")
            
        def test_get(self):
            self.client.login(username="test@test.com", password="test")
            response = self.client.get(self.event_edit_url, follow=True)
            self.failUnlessEqual(response.template[0].name, "events/edit.html")
            event = response.context["event"]
            self.failUnlessEqual(event.event_type, self.event_type)
            self.failUnlessEqual(event.where, "123 Garden Street")
            self.failUnlessEqual(event.location.name, "Ashaway")
            self.failUnlessEqual(event.location.st, "RI")
            self.failUnlessEqual(event.location.zipcode, "02804")
            self.failUnlessEqual(event.when, datetime.date(2050, 8, 14))
            self.failUnlessEqual(event.start, datetime.time(6, 0))
            self.failUnlessEqual(event.end, datetime.time(8, 0))
            self.failUnlessEqual(event.details, "You can park on the street.  My apartment is on the second floor.")
            self.failUnlessEqual(event.is_private, False)
            
        def test_missing_required(self):
            self.client.login(username="test@test.com", password="test")
            response = self.client.post(self.event_edit_url, {"event_type": "", "where": "",
                "city": "", "state": "", "zipcode": "", "when": "", 
                "start": "", "end": "", "details": "", "is_private": "False"}, follow=True)
            self.failUnlessEqual(response.template[0].name, "events/edit.html")
            errors = response.context["form"].errors
            self.failUnlessEqual(len(errors), 7)
            self.failUnless("event_type" in errors)
            self.failUnless("where" in errors)
            self.failUnless("when" in errors)
            self.failUnless("start" in errors)
            self.failUnless("end" in errors)
            self.failUnless("details" in errors)
            
        def test_change_event(self):
            self.client.login(username="test@test.com", password="test")
            response = self.client.post(self.event_edit_url, {"event_type": self.event_type.pk, 
                "where": "11 Fake St.", "city": "ashaway", "state": "RI", "zipcode": "02804", "when": "2050-09-09", 
                "start": "10:00", "end": "11:00", "details": "test", "is_private": "True"}, follow=True)
            self.failUnlessEqual(response.template[0].name, "events/show.html")
            event = response.context["event"]
            self.failUnlessEqual(event.event_type, self.event_type)
            self.failUnlessEqual(event.where, "11 Fake St.")
            self.failUnlessEqual(event.location.name, "Ashaway")
            self.failUnlessEqual(event.location.st, "RI")
            self.failUnlessEqual(event.location.zipcode, "02804")
            self.failUnlessEqual(event.when, datetime.date(2050, 9, 9))
            self.failUnlessEqual(event.start, datetime.time(10, 0))
            self.failUnlessEqual(event.end, datetime.time(11, 0))
            self.failUnlessEqual(event.details, "test")
            self.failUnlessEqual(event.is_private, True)
            
class EventGuestsViewTest(TestCase):
    fixtures = ["test_geo_02804.json", "test_events.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.event_type = EventType.objects.get(pk=1)
        self.event = Event.objects.get(pk=1)
        self.event_guests_url = reverse("event-guests", args=[self.event.id])

    def test_login_required(self):
        response = self.client.get(self.event_guests_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/register.html")
        
    def test_get(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.event_guests_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests.html")
        guests = response.context["event"].guest_set.all()
        self.failUnlessEqual(len(guests), 6)
        
    def test_missing_required(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_guests_url, {"action": ""}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests.html")
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 2)
        self.failUnless("action" in errors)
        self.failUnless("guests" in errors)
        
    def test_missing_email(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_guests_url, {"action": "3_EI", 
            "guests": ("5", "6",)}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests.html")
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 1)
        self.failUnless("__all__" in errors)
        
    def test_valid_action(self):
        self.client.login(username="test@test.com", password="test")
        guest_5 = Guest.objects.get(pk=5)
        guest_6 = Guest.objects.get(pk=6)
        self.failUnlessEqual(guest_5.is_host, False)
        self.failUnlessEqual(guest_6.is_host, False)
        response = self.client.post(self.event_guests_url, {"action": "4_MH", 
            "guests": ("5", "6",)}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests.html")
        guest_5 = Guest.objects.get(pk=5)
        guest_6 = Guest.objects.get(pk=6)
        self.failUnlessEqual(guest_5.is_host, True)
        self.failUnlessEqual(guest_6.is_host, True)
        
    def test_action_redirect(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_guests_url, {"action": "3_EI", 
            "guests": ("6",)}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests_add.html")
        