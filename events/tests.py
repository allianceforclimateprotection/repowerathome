import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from utils import hash_val

from geo.models import Location
from invite.models import Invitation, make_token

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
        guest = Guest.objects.get(first_name="Jane", last_name="Doe")
        guest.email = hacker.email
        guest.save()
        self.failUnlessEqual(self.event.has_manager_privileges(hacker), False)
        guest.is_host = True
        guest.save()
        self.failUnlessEqual(self.event.has_manager_privileges(hacker), True)
        
    def test_confirmed_guests(self):
        self.failUnlessEqual(self.event.confirmed_guests(), 1)
        alex = Guest.objects.get(first_name="Alex", last_name="Smith")
        alex.rsvp_status = "A"
        alex.save()
        self.failUnlessEqual(self.event.confirmed_guests(), 2)
        jane = Guest.objects.get(first_name="Jane", last_name="Doe")
        jane.rsvp_status = "N"
        jane.save()
        self.failUnlessEqual(self.event.confirmed_guests(), 1)
        
    def test_outstanding_invitations(self):
        self.failUnlessEqual(self.event.outstanding_invitations(), 2)
        jon = Guest.objects.get(first_name="Jon", last_name="Doe")
        jon.rsvp_status = "M"
        jon.save()
        self.failUnlessEqual(self.event.outstanding_invitations(), 1)
        
    def test_place(self):
        self.failUnlessEqual(self.event.place(), "123 Garden Street Ashaway, RI")
        
    def test_is_token_valid(self):
        token = make_token()
        invite = Invitation.objects.create(user=self.creator, email="test@email.com", 
            token=token, content_object=self.event)
        self.failUnless(self.event.is_token_valid(token))
        new_event = Event.objects.create(creator=self.creator, event_type=self.event_type,
            location=self.ashaway, when=datetime.date(2050, 9, 9), start=datetime.time(9,0),
            duration=90, details="test")
        self.failUnless(not new_event.is_token_valid(token))

class GuestTest(TestCase):
    fixtures = ["test_events.json",]
    
    def setUp(self):
        self.jane = Guest.objects.get(first_name="Jane", last_name="Doe")
        self.alex = Guest.objects.get(first_name="Alex", last_name="Smith")
        self.jon = Guest.objects.get(first_name="Jon", last_name="Doe")
        self.me = Guest.objects.get(email="me@gmail.com")
        self.jonathan = Guest.objects.get(first_name="Jonathan")
        self.mike = Guest.objects.get(first_name="Mike", last_name="Roberts")
        
    def test_status(self):
        self.failUnlessEqual(self.jane.status(), "Attending")
        self.failUnlessEqual(self.alex.status(), "Not Attending")
        self.failUnlessEqual(self.jon.status(), "Invited May 18")
        self.failUnlessEqual(self.me.status(), "Invited Mar 12")
        self.failUnlessEqual(self.jonathan.status(), "Added Feb 2")
        self.failUnlessEqual(self.mike.status(), "Maybe Attending")
        
    def test_needs_more_info(self):
        self.failUnlessEqual(self.jane.needs_more_info(), False)
        self.failUnlessEqual(self.alex.needs_more_info(), False)
        self.failUnlessEqual(self.jon.needs_more_info(), False)
        self.failUnlessEqual(self.me.needs_more_info(), True)
        self.failUnlessEqual(self.jonathan.needs_more_info(), True)
        self.failUnlessEqual(self.mike.needs_more_info(), False)
        
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
            "start_hour": "", "start_minute": "", "start_meridiem": "",  "duration": "", 
            "details": "", "is_private": "False", "limit": ""}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/create.html")
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 5)
        self.failUnless("__all__" in errors)
        self.failUnless("event_type" in errors)
        self.failUnless("where" in errors)
        self.failUnless("when" in errors)
        self.failUnless("start" in errors)
        
    def test_invalid_zipcode(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "", "state": "", "zipcode": "99999", "when": "2050-09-09", 
            "start_hour": "10", "start_minute": "00", "start_meridiem": "p.m.", "duration": "120", 
            "details": "test", "is_private": "False", "limit": ""}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/create.html")
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 1)
        self.failUnless("zipcode" in errors)
        
    def test_invalid_city_state(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "ashawa", "state": "RI", "zipcode": "", "when": "2050-09-09", 
            "start_hour": "10", "start_minute": "00", "start_meridiem": "p.m.", "duration": "120", 
            "details": "test", "is_private": "False", "limit": ""}, follow=True)
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 1)
        error = errors["__all__"][0]
        self.failUnless("place" in error)
        
    def test_missing_city_state_and_zipcode(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "", "state": "", "zipcode": "", "when": "2050-09-09", 
            "start_hour": "10", "start_minute": "00", "start_meridiem": "p.m.", "duration": "120", 
            "details": "test", "is_private": "False", "limit": ""}, follow=True)
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
            "start_hour": "10", "start_minute": "00", "start_meridiem": "p.m.", "duration": "120", 
            "details": "test", "is_private": "False", "limit": "20"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/show.html")
        event = response.context["event"]
        self.failUnlessEqual(event.event_type, self.event_type)
        self.failUnlessEqual(event.where, "11 Fake St.")
        self.failUnlessEqual(event.location.name, "Ashaway")
        self.failUnlessEqual(event.location.st, "RI")
        self.failUnlessEqual(event.location.zipcode, "02804")
        self.failUnlessEqual(event.when, datetime.date(2050, 9, 9))
        self.failUnlessEqual(event.start, datetime.time(22, 0))
        self.failUnlessEqual(event.duration, 120)
        self.failUnlessEqual(event.details, "test")
        self.failUnlessEqual(event.is_private, False)
        self.failUnlessEqual(event.limit, 20)
        
    def test_valid_zipcode_create(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "", "state": "", "zipcode": "02804", "when": "2050-09-09", 
            "start_hour": "10", "start_minute": "00", "start_meridiem": "p.m.", "duration": "120", 
            "details": "test", "is_private": "True", "limit": "20"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/show.html")
        event = response.context["event"]
        self.failUnlessEqual(event.event_type, self.event_type)
        self.failUnlessEqual(event.where, "11 Fake St.")
        self.failUnlessEqual(event.location.name, "Ashaway")
        self.failUnlessEqual(event.location.st, "RI")
        self.failUnlessEqual(event.location.zipcode, "02804")
        self.failUnlessEqual(event.when, datetime.date(2050, 9, 9))
        self.failUnlessEqual(event.start, datetime.time(22, 0))
        self.failUnlessEqual(event.duration, 120)
        self.failUnlessEqual(event.details, "test")
        self.failUnlessEqual(event.is_private, True)
        self.failUnlessEqual(event.limit, 20)
        
    def test_valid_city_state_zipcode_create(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_create_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "ashaway", "state": "RI", "zipcode": "02804", "when": "2050-09-09", 
            "start_hour": "10", "start_minute": "00", "start_meridiem": "p.m.", "duration": "120", 
            "details": "test", "is_private": "True", "limit": "20"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/show.html")
        event = response.context["event"]
        self.failUnlessEqual(event.event_type, self.event_type)
        self.failUnlessEqual(event.where, "11 Fake St.")
        self.failUnlessEqual(event.location.name, "Ashaway")
        self.failUnlessEqual(event.location.st, "RI")
        self.failUnlessEqual(event.location.zipcode, "02804")
        self.failUnlessEqual(event.when, datetime.date(2050, 9, 9))
        self.failUnlessEqual(event.start, datetime.time(22, 0))
        self.failUnlessEqual(event.duration, 120)
        self.failUnlessEqual(event.details, "test")
        self.failUnlessEqual(event.is_private, True)
        self.failUnlessEqual(event.limit, 20)
        
class EventShowViewTest(TestCase):
    fixtures = ["test_geo_02804.json", "test_events.json"]
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.event_type = EventType.objects.get(pk=1)
        self.event = Event.objects.get(pk=1)
        self.event_show_url = reverse("event-show", args=[self.event.id])

    def test_invalid_event(self):
        response = self.client.get(reverse("event-show", args=[999]))
        self.failUnlessEqual(response.status_code, 404)
        
    def test_get(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.event_show_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/rsvp.html")
        
    def test_not_a_guest_and_private(self):
        self.event.is_private = True
        self.event.save()
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.event_show_url, follow=True)
        self.failUnlessEqual(response.status_code, 403)
        
    def test_invalid_token(self):
        self.event.is_private = True
        self.event.save()
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(reverse("event-invite", args=[self.event.id, "81234f0a90c7ef4"]), follow=True)
        self.failUnlessEqual(response.status_code, 403)
        
    def test_guest_and_private(self):
        self.event.is_private = True
        self.event.save()
        Guest.objects.create(event=self.event, first_name="test", email="test@test.com", user=self.user)
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.event_show_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/rsvp.html")
        event = response.context["event"]
        self.failUnlessEqual(event.event_type, self.event_type)
        self.failUnlessEqual(event.where, "123 Garden Street")
        self.failUnlessEqual(event.location.name, "Ashaway")
        self.failUnlessEqual(event.location.st, "RI")
        self.failUnlessEqual(event.location.zipcode, "02804")
        self.failUnlessEqual(event.when, datetime.date(2050, 8, 14))
        self.failUnlessEqual(event.start, datetime.time(6, 0))
        self.failUnlessEqual(event.duration, 90)
        self.failUnlessEqual(event.details, "You can park on the street.  My apartment is on the second floor.")
        self.failUnlessEqual(event.is_private, True)
        
    def test_valid_token(self):
        self.event.is_private = True
        self.event.save()
        token = make_token()
        invite = Invitation.objects.create(user=self.user, email="test@email.com", 
            token=token, content_object=self.event)
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(reverse("event-invite", args=[self.event.id, invite.token]), follow=True)
        self.failUnlessEqual(response.template[0].name, "events/rsvp.html")
        event = response.context["event"]
        self.failUnlessEqual(event.event_type, self.event_type)
        self.failUnlessEqual(event.where, "123 Garden Street")
        self.failUnlessEqual(event.location.name, "Ashaway")
        self.failUnlessEqual(event.location.st, "RI")
        self.failUnlessEqual(event.location.zipcode, "02804")
        self.failUnlessEqual(event.when, datetime.date(2050, 8, 14))
        self.failUnlessEqual(event.start, datetime.time(6, 0))
        self.failUnlessEqual(event.duration, 90)
        self.failUnlessEqual(event.details, "You can park on the street.  My apartment is on the second floor.")
        self.failUnlessEqual(event.is_private, True)
        
class EventEditViewTest(TestCase):
    fixtures = ["test_geo_02804.json", "test_events.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.event_type = EventType.objects.get(pk=1)
        self.event = Event.objects.get(pk=1)
        self.event.creator = self.user
        self.event.save()
        self.event_edit_url = reverse("event-edit", args=[self.event.id])
        
    def test_login_required(self):
        response = self.client.get(self.event_edit_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        
    def test_no_permissions(self):
        self.hacker = User.objects.create_user(username="2", email="hacker@test.com", password="test")
        self.client.login(username="hacker@test.com", password="test")
        response = self.client.get(self.event_edit_url, follow=True)
        self.failUnlessEqual(response.status_code, 403)
        
    def test_invalid_event(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(reverse("event-edit", args=[999]))
        self.failUnlessEqual(response.status_code, 404)
        
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
        self.failUnlessEqual(event.duration, 90)
        self.failUnlessEqual(event.details, "You can park on the street.  My apartment is on the second floor.")
        self.failUnlessEqual(event.is_private, False)
        
    def test_missing_required(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_edit_url, {"event_type": "", "where": "",
            "city": "", "state": "", "zipcode": "", "when": "", 
            "start_hour": "", "start_minute": "", "start_meridiem": "",
            "duration": "", "details": "", "is_private": "False", "limit": ""}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/edit.html")
        errors = response.context["form"].errors
        self.failUnlessEqual(len(errors), 5)
        self.failUnless("__all__" in errors)
        self.failUnless("event_type" in errors)
        self.failUnless("where" in errors)
        self.failUnless("when" in errors)
        self.failUnless("start" in errors)
        
    def test_change_event(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_edit_url, {"event_type": self.event_type.pk, 
            "where": "11 Fake St.", "city": "ashaway", "state": "RI", "zipcode": "02804", "when": "2050-09-09", 
            "start_hour": "10", "start_minute": "00", "start_meridiem": "a.m.",
            "duration": "90", "details": "test", "is_private": "True", "limit": "30"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/show.html")
        event = response.context["event"]
        self.failUnlessEqual(event.event_type, self.event_type)
        self.failUnlessEqual(event.where, "11 Fake St.")
        self.failUnlessEqual(event.location.name, "Ashaway")
        self.failUnlessEqual(event.location.st, "RI")
        self.failUnlessEqual(event.location.zipcode, "02804")
        self.failUnlessEqual(event.when, datetime.date(2050, 9, 9))
        self.failUnlessEqual(event.start, datetime.time(10, 0))
        self.failUnlessEqual(event.duration, 90)
        self.failUnlessEqual(event.details, "test")
        self.failUnlessEqual(event.is_private, True)
        self.failUnlessEqual(event.limit, 30)
            
class EventGuestsViewTest(TestCase):
    fixtures = ["test_geo_02804.json", "test_events.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.event_type = EventType.objects.get(pk=1)
        self.event = Event.objects.get(pk=1)
        self.event.creator = self.user
        self.event.save()
        self.event_guests_url = reverse("event-guests", args=[self.event.id])

    def test_login_required(self):
        response = self.client.get(self.event_guests_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        
    def test_no_permissions(self):
        self.hacker = User.objects.create_user(username="2", email="hacker@test.com", password="test")
        self.client.login(username="hacker@test.com", password="test")
        response = self.client.get(self.event_guests_url, follow=True)
        self.failUnlessEqual(response.status_code, 403)
        
    def test_invalid_event(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(reverse("event-guests", args=[999]))
        self.failUnlessEqual(response.status_code, 404)
        
    def test_get(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.event_guests_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests.html")
        guests = response.context["event"].guest_set.all()
        self.failUnlessEqual(len(guests), 7)
        
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
        response = self.client.post(self.event_guests_url, {"action": "4_EI", 
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
        response = self.client.post(self.event_guests_url, {"action": "7_MH", 
            "guests": ("5", "6",)}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests.html")
        guest_5 = Guest.objects.get(pk=5)
        guest_6 = Guest.objects.get(pk=6)
        self.failUnlessEqual(guest_5.is_host, True)
        self.failUnlessEqual(guest_6.is_host, True)
        
    def test_action_redirect(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_guests_url, {"action": "4_EI", 
            "guests": ("6",)}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests_add.html")
        
class EventGuestsAddViewTest(TestCase):
    fixtures = ["test_geo_02804.json", "test_events.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.event_type = EventType.objects.get(pk=1)
        self.event = Event.objects.get(pk=1)
        self.event.creator = self.user
        self.event.save()
        self.event_guests_add_url = reverse("event-guests-add", args=[self.event.id])
        
    def test_login_required(self):
        response = self.client.get(self.event_guests_add_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")

    def test_no_permissions(self):
        self.hacker = User.objects.create_user(username="2", email="hacker@test.com", password="test")
        self.client.login(username="hacker@test.com", password="test")
        response = self.client.get(self.event_guests_add_url, follow=True)
        self.failUnlessEqual(response.status_code, 403)

    def test_invalid_event(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(reverse("event-guests-add", args=[999]))
        self.failUnlessEqual(response.status_code, 404)
        
    def test_get(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.event_guests_add_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests_add.html")
        self.failUnless(response.context["guest_invite_form"])
        self.failUnless(response.context["guest_add_form"])
        
    def test_missing_required(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_guests_add_url, {"first_name": "", "last_name": "",
            "email": "", "phone": "", "rsvp_status": ""}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests_add.html")
        errors = response.context["guest_add_form"].errors
        self.failUnlessEqual(len(errors), 2)
        self.failUnless("first_name" in errors)
        self.failUnless("rsvp_status" in errors)
        
    def test_invalid_email(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_guests_add_url, {"first_name": "Jon", "last_name": "",
            "email": "jon@", "phone": "", "rsvp_status": "N"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests_add.html")
        errors = response.context["guest_add_form"].errors
        self.failUnlessEqual(len(errors), 1)
        self.failUnless("email" in errors)
    
    def test_duplicate_email(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_guests_add_url, {"first_name": "Jon", "last_name": "Doe",
            "email": "jd@email.com", "phone": "", "rsvp_status": "A"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests_add.html")
        errors = response.context["guest_add_form"].errors
        self.failUnlessEqual(len(errors), 1)
        self.failUnless("email" in errors)
        
    def test_valid_post(self):
        self.client.login(username="test@test.com", password="test")
        self.failUnlessEqual(self.event.guest_set.all().count(), 7)
        response = self.client.post(self.event_guests_add_url, {"first_name": "Jon", "last_name": "",
            "email": "jon@gmail.com", "phone": "", "rsvp_status": "N"}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests.html")
        event = response.context["event"]
        guests = event.guest_set.all()
        self.failUnlessEqual(len(guests), 8)
        jon = guests[7]
        self.failUnlessEqual(jon.first_name, "Jon")
        self.failUnlessEqual(jon.email, "jon@gmail.com")
        self.failUnlessEqual(jon.rsvp_status, "N")
        
class EventGuestsInviteViewTest(TestCase):
    fixtures = ["test_geo_02804.json", "test_events.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.event_type = EventType.objects.get(pk=1)
        self.event = Event.objects.get(pk=1)
        self.event.creator = self.user
        self.event.save()
        self.event_content_type = ContentType.objects.get(app_label="events", model="event")
        self.event_guests_invite_url = reverse("event-guests-invite", args=[self.event.id])
        
    def test_login_required(self):
        response = self.client.get(self.event_guests_invite_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")

    def test_no_permissions(self):
        self.hacker = User.objects.create_user(username="2", email="hacker@test.com", password="test")
        self.client.login(username="hacker@test.com", password="test")
        response = self.client.get(self.event_guests_invite_url, follow=True)
        self.failUnlessEqual(response.status_code, 403)

    def test_invalid_event(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(reverse("event-guests-invite", args=[999]))
        self.failUnlessEqual(response.status_code, 404)
        
    def test_get(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.event_guests_invite_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests_add.html")
        self.failUnless(response.context["guest_invite_form"])
        self.failUnless(response.context["guest_add_form"])
        
    def test_missing_required(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_guests_invite_url, {"emails": "", "note": "something",
            "rsvp_notification": "", "copy_me": "", "signature": "",}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests_add.html")
        errors = response.context["guest_invite_form"].errors
        self.failUnlessEqual(len(errors), 2)
        self.failUnless("emails" in errors)
        self.failUnless("signature" in errors)
        
    def test_invalid_email(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_guests_invite_url, {"emails": "jon@", "note": "",
            "rsvp_notification": "", "copy_me": "", 
            "signature": hash_val((self.event_content_type, self.event.pk,)),}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests_add.html")
        errors = response.context["guest_invite_form"].errors
        self.failUnlessEqual(len(errors), 1)
        self.failUnless("emails" in errors)
        
    def test_invalid_email_list(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(self.event_guests_invite_url, {"emails": "jon@gmail.com eric@gmail.com", 
            "note": "", "rsvp_notification": "", "copy_me": "", 
            "signature": hash_val((self.event_content_type, self.event.pk,)),}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests_add.html")
        errors = response.context["guest_invite_form"].errors
        self.failUnlessEqual(len(errors), 1)
        self.failUnless("emails" in errors)
        
    def test_single_invite(self):
        self.client.login(username="test@test.com", password="test")
        self.failUnlessEqual(self.event.guest_set.all().count(), 7)
        response = self.client.post(self.event_guests_invite_url, {"emails": "jon@gmail.com", 
            "note": "", "content_type": self.event_content_type.pk, "object_pk": self.event.pk,
            "signature": hash_val((self.event_content_type, self.event.pk,)),}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests.html")
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["jon@gmail.com"])
        self.failUnlessEqual(email.subject, "Invitation from %s to Repower at Home" % self.user.get_full_name())
        event = response.context["event"]
        guests = event.guest_set.all()
        self.failUnlessEqual(len(guests), 8)
        jon = guests[7]
        self.failUnlessEqual(jon.first_name, "")
        self.failUnlessEqual(jon.email, "jon@gmail.com")
        
    def test_multiple_invite(self):
        self.client.login(username="test@test.com", password="test")
        self.failUnlessEqual(self.event.guest_set.all().count(), 7)
        response = self.client.post(self.event_guests_invite_url, {"emails": "jon@gmail.com,eric@gmail.com", 
            "note": "", "content_type": self.event_content_type.pk, "object_pk": self.event.pk,
            "signature": hash_val((self.event_content_type, self.event.pk,)),}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests.html")
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["eric@gmail.com"])
        self.failUnlessEqual(email.subject, "Invitation from %s to Repower at Home" % self.user.get_full_name())
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["jon@gmail.com"])
        self.failUnlessEqual(email.subject, "Invitation from %s to Repower at Home" % self.user.get_full_name())
        event = response.context["event"]
        guests = event.guest_set.all()
        self.failUnlessEqual(len(guests), 9)
        jon = guests[7]
        self.failUnlessEqual(jon.first_name, "")
        self.failUnlessEqual(jon.email, "jon@gmail.com")
        eric = guests[8]
        self.failUnlessEqual(eric.first_name, "")
        self.failUnlessEqual(eric.email, "eric@gmail.com")
        
    def test_copy_me_email(self):
        self.client.login(username="test@test.com", password="test")
        self.failUnlessEqual(self.event.guest_set.all().count(), 7)
        response = self.client.post(self.event_guests_invite_url, {"emails": "jon@gmail.com", "copy_me": True,
            "note": "", "content_type": self.event_content_type.pk, "object_pk": self.event.pk,
            "signature": hash_val((self.event_content_type, self.event.pk,)),}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests.html")
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["test@test.com"])
        self.failUnlessEqual(email.subject, "Invitation from %s to Repower at Home" % self.user.get_full_name())
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["jon@gmail.com"])
        self.failUnlessEqual(email.subject, "Invitation from %s to Repower at Home" % self.user.get_full_name())
        event = response.context["event"]
        guests = event.guest_set.all()
        self.failUnlessEqual(len(guests), 8)
        jon = guests[7]
        self.failUnlessEqual(jon.first_name, "")
        self.failUnlessEqual(jon.email, "jon@gmail.com")
        
    def test_duplicate_email(self):
        self.client.login(username="test@test.com", password="test")
        self.failUnlessEqual(self.event.guest_set.all().count(), 7)
        response = self.client.post(self.event_guests_invite_url, {"emails": "jd@email.com", 
            "note": "", "content_type": self.event_content_type.pk, "object_pk": self.event.pk,
            "signature": hash_val((self.event_content_type, self.event.pk,)),}, follow=True)
        self.failUnlessEqual(response.template[0].name, "events/guests.html")
        email = mail.outbox.pop()
        self.failUnlessEqual(email.to, ["jd@email.com"])
        self.failUnlessEqual(email.subject, "Invitation from %s to Repower at Home" % self.user.get_full_name())
        event = response.context["event"]
        guests = event.guest_set.all()
        self.failUnlessEqual(len(guests), 7)
        
class EventGuestsEditNameViewTest(TestCase):
    fixtures = ["test_geo_02804.json", "test_events.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.event_type = EventType.objects.get(pk=1)
        self.event = Event.objects.get(pk=1)
        self.guest = Guest.objects.get(pk=1)
        self.event.creator = self.user
        self.event.save()
        self.event_guests_edit_url = reverse("event-guests-edit-name", args=[self.event.id, self.guest.id])
        
    def test_login_required(self):
        response = self.client.get(self.event_guests_edit_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        
    def test_get(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.event_guests_edit_url, follow=True)
        self.failUnlessEqual(response.status_code, 405)
        
    def test_no_permissions(self):
        self.hacker = User.objects.create_user(username="2", email="hacker@test.com", password="test")
        self.client.login(username="hacker@test.com", password="test")
        response = self.client.post(self.event_guests_edit_url, {}, follow=True)
        self.failUnlessEqual(response.status_code, 403)
        
    def test_invalid_event(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(reverse("event-guests-edit-name", args=[999,self.guest.id]))
        self.failUnlessEqual(response.status_code, 404)
        
    def test_invalid_guest(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(reverse("event-guests-edit-name", args=[self.event.id,999]))
        self.failUnlessEqual(response.status_code, 404)
    
    def test_invalid_event_guest_pair(self):
        ashaway = Location.objects.get(zipcode="02804")
        new_event = Event.objects.create(creator=self.user, event_type=self.event_type,
            location=ashaway, when=datetime.date(2050, 9, 9), start=datetime.time(9,0),
            duration=60, details="test")
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(reverse("event-guests-edit-name", args=[new_event.id,self.guest.id]))
        self.failUnlessEqual(response.status_code, 403)
        
    def test_set_first_name(self):
        self.client.login(username="test@test.com", password="test")
        self.failUnlessEqual(self.guest.first_name, "Jane")
        self.failUnlessEqual(self.guest.last_name, "Doe")
        response = self.client.post(self.event_guests_edit_url, {"value": "Jimmy"}, follow=True)
        self.guest = Guest.objects.get(pk=1)
        self.failUnlessEqual(self.guest.first_name, "Jimmy")
        self.failUnlessEqual(self.guest.last_name, "")
        self.failUnlessEqual(response.get("content-type", 1), "text/json")
        self.failUnlessEqual(response.template[1].name, "events/_guest_row.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        
    def test_set_name(self):
        self.client.login(username="test@test.com", password="test")
        self.failUnlessEqual(self.guest.first_name, "Jane")
        self.failUnlessEqual(self.guest.last_name, "Doe")
        response = self.client.post(self.event_guests_edit_url, {"value": "Jimmy Smith Williams"}, follow=True)
        self.guest = Guest.objects.get(pk=1)
        self.failUnlessEqual(self.guest.first_name, "Jimmy")
        self.failUnlessEqual(self.guest.last_name, "Smith Williams")
        self.failUnlessEqual(response.get("content-type", 1), "text/json")
        self.failUnlessEqual(response.template[1].name, "events/_guest_row.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        
class EventGuestsEditEmailViewTest(TestCase):
    fixtures = ["test_geo_02804.json", "test_events.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.event_type = EventType.objects.get(pk=1)
        self.event = Event.objects.get(pk=1)
        self.guest = Guest.objects.get(pk=1)
        self.event.creator = self.user
        self.event.save()
        self.event_guests_edit_url = reverse("event-guests-edit-email", args=[self.event.id, self.guest.id])
        
    def test_login_required(self):
        response = self.client.get(self.event_guests_edit_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")
        
    def test_get(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.event_guests_edit_url, follow=True)
        self.failUnlessEqual(response.status_code, 405)
        
    def test_no_permissions(self):
        self.hacker = User.objects.create_user(username="2", email="hacker@test.com", password="test")
        self.client.login(username="hacker@test.com", password="test")
        response = self.client.post(self.event_guests_edit_url, {}, follow=True)
        self.failUnlessEqual(response.status_code, 403)
        
    def test_invalid_event(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(reverse("event-guests-edit-name", args=[999,self.guest.id]))
        self.failUnlessEqual(response.status_code, 404)
        
    def test_invalid_guest(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(reverse("event-guests-edit-name", args=[self.event.id,999]))
        self.failUnlessEqual(response.status_code, 404)
    
    def test_invalid_event_guest_pair(self):
        ashaway = Location.objects.get(zipcode="02804")
        new_event = Event.objects.create(creator=self.user, event_type=self.event_type,
            location=ashaway, when=datetime.date(2050, 9, 9), start=datetime.time(9,0),
            duration=180, details="test")
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(reverse("event-guests-edit-name", args=[new_event.id,self.guest.id]))
        self.failUnlessEqual(response.status_code, 403)
        
    def test_set_invalid_email(self):
        self.client.login(username="test@test.com", password="test")
        self.failUnlessEqual(self.guest.email, "jd@email.com")
        response = self.client.post(self.event_guests_edit_url, {"value": "jimmy@"}, follow=True)
        self.guest = Guest.objects.get(pk=1)
        self.failUnlessEqual(self.guest.email, "jd@email.com")
        self.failUnlessEqual(response.get("content-type", 1), "text/json")
        self.failUnlessEqual(response.template[1].name, "events/_guest_row.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("error" in message.tags)
        
    def test_set_duplicate_email(self):
        self.client.login(username="test@test.com", password="test")
        self.failUnlessEqual(self.guest.email, "jd@email.com")
        response = self.client.post(self.event_guests_edit_url, {"value": "jondoe@email.com"}, follow=True)
        self.guest = Guest.objects.get(pk=1)
        self.failUnlessEqual(self.guest.email, "jd@email.com")
        self.failUnlessEqual(response.get("content-type", 1), "text/json")
        self.failUnlessEqual(response.template[1].name, "events/_guest_row.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("error" in message.tags)
        
    def test_set_email(self):
        self.client.login(username="test@test.com", password="test")
        self.failUnlessEqual(self.guest.email, "jd@email.com")
        response = self.client.post(self.event_guests_edit_url, {"value": "jimmy@email.com"}, follow=True)
        self.guest = Guest.objects.get(pk=1)
        self.failUnlessEqual(self.guest.email, "jimmy@email.com")
        self.failUnlessEqual(response.get("content-type", 1), "text/json")
        self.failUnlessEqual(response.template[1].name, "events/_guest_row.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)
        
class EventGuestsEditPhoneViewTest(TestCase):
    fixtures = ["test_geo_02804.json", "test_events.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="1", email="test@test.com", password="test")
        self.event_type = EventType.objects.get(pk=1)
        self.event = Event.objects.get(pk=1)
        self.guest = Guest.objects.get(pk=1)
        self.event.creator = self.user
        self.event.save()
        self.event_guests_edit_url = reverse("event-guests-edit-phone", args=[self.event.id, self.guest.id])

    def test_login_required(self):
        response = self.client.get(self.event_guests_edit_url, follow=True)
        self.failUnlessEqual(response.template[0].name, "registration/login.html")

    def test_get(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.get(self.event_guests_edit_url, follow=True)
        self.failUnlessEqual(response.status_code, 405)

    def test_no_permissions(self):
        self.hacker = User.objects.create_user(username="2", email="hacker@test.com", password="test")
        self.client.login(username="hacker@test.com", password="test")
        response = self.client.post(self.event_guests_edit_url, {}, follow=True)
        self.failUnlessEqual(response.status_code, 403)

    def test_invalid_event(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(reverse("event-guests-edit-name", args=[999,self.guest.id]))
        self.failUnlessEqual(response.status_code, 404)

    def test_invalid_guest(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(reverse("event-guests-edit-name", args=[self.event.id,999]))
        self.failUnlessEqual(response.status_code, 404)

    def test_invalid_event_guest_pair(self):
        ashaway = Location.objects.get(zipcode="02804")
        new_event = Event.objects.create(creator=self.user, event_type=self.event_type,
            location=ashaway, when=datetime.date(2050, 9, 9), start=datetime.time(9,0),
            duration=60, details="test")
        self.client.login(username="test@test.com", password="test")
        response = self.client.post(reverse("event-guests-edit-name", args=[new_event.id,self.guest.id]))
        self.failUnlessEqual(response.status_code, 403)

    def test_set_phone(self):
        self.client.login(username="test@test.com", password="test")
        self.failUnlessEqual(self.guest.phone, "")
        response = self.client.post(self.event_guests_edit_url, {"value": "555-555-5555"}, follow=True)
        self.guest = Guest.objects.get(pk=1)
        self.failUnlessEqual(self.guest.phone, "555-555-5555")
        self.failUnlessEqual(response.get("content-type", 1), "text/json")
        self.failUnlessEqual(response.template[1].name, "events/_guest_row.html")
        message = iter(response.context["messages"]).next()
        self.failUnless("success" in message.tags)