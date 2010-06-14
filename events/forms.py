import datetime
import hashlib
import re

from django import forms
from django.forms import formsets
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template import Context, loader

from geo.models import Location
from invite.models import Invitation
from invite.forms import InviteForm
from invite.fields import MultiEmailField

from models import EventType, Event, Guest, Survey, Challenge, Commitment, rsvp_recieved
from widgets import SelectTimeWidget

STATES = ("AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "IA", "ID", 
    "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", 
    "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", 
    "UT", "VA", "VT", "WA", "WI", "WV", "WY",)
    
def _times():
    times = []
    for hour_24 in range(0,24):
        for minute in [0,15,30,45]:
            hour_12 = hour_24 % 12
            if hour_12 == 0: hour_12 = 12
            meridiem = "am" if hour_24 / 12 == 0 else "pm"
            times.append(("%0.2d:%0.2d:00" % (hour_24, minute), 
                "%0.2d:%0.2d%s" % (hour_12, minute, meridiem)))
    return times
TIMES = _times()

def _durations():
    durations = []
    hours = range(1,3)
    for hour in hours:
        for minute in [0,15,30,45]:
            durations.append(("%s" % (hour*60+minute), "%0.2d:%0.2d" % (hour, minute)))
    next_hour = hours[-1] + 1
    durations.append(("%s" % (next_hour*60), "%0.2d:00" % next_hour))
    return durations
DURATIONS = _durations()

class EventForm(forms.ModelForm):
    where = forms.CharField(max_length=100, label="Address")
    city = forms.CharField(required=False, max_length=50)
    state = forms.ChoiceField(required=False, choices=[("", "state")]+[(state, state) for state in STATES])
    zipcode = forms.CharField(required=False, max_length=5)
    is_private = forms.ChoiceField(choices=((True, "Yes"), (False, "No")), initial=False,
        widget=forms.RadioSelect, help_text="If your event is kept private, only individuals\
            who receive an invite email will be able to RSVP.")
    
    class Meta:
        model = Event
        fields = ["event_type", "where", "city", "state", "zipcode", "when", "start", "duration", 
            "details", "is_private", "limit"]
        widgets = {
            "event_type": forms.RadioSelect,
            "when": forms.TextInput(attrs={"class": "datepicker future_date_warning"}),
            "start": SelectTimeWidget(minute_step=15, twelve_hr=True, use_seconds=False),
            "duration": forms.Select(choices=[("", "---")]+DURATIONS)
        }
        
    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if self.instance.location:
            self.fields["city"].initial = self.instance.location.name
            self.fields["state"].initial = self.instance.location.st
            self.fields["zipcode"].initial = self.instance.location.zipcode
        self.user = user
        if not self.user.has_perm("host_any_event_type"):
            self.fields["event_type"].initial = EventType.objects.get(name="Energy Meeting").pk
            self.fields["event_type"].widget = forms.HiddenInput()
        
    def clean_zipcode(self):
        data = self.cleaned_data["zipcode"]
        if data:
            try:
                self.cleaned_data["location"] = Location.objects.get(zipcode=data)
            except Location.DoesNotExist:
                raise forms.ValidationError("Invalid zipcode %s" % data)
        return data
        
    def clean(self):
        city = self.cleaned_data.get("city", None)
        state = self.cleaned_data.get("state", None)
        if city and state:
            locations = Location.objects.filter(name__iexact=city, st=state)
            if not locations:
                raise forms.ValidationError("Invalid place %s, %s" % (city, state))
            self.cleaned_data["location"] = locations[0]
        
        if not "location" in self.cleaned_data and not "zipcode" in self.errors:
            raise forms.ValidationError("You must specify city and state or a zipcode")
        return self.cleaned_data
        
    def save(self, *args, **kwargs):
        self.instance.creator = self.user
        self.instance.location = self.cleaned_data["location"]
        return super(EventForm, self).save(*args, **kwargs)
    
class GuestInviteForm(InviteForm):
    emails = MultiEmailField(label="Email addresses", required=True, widget=forms.Textarea)
    rsvp_notification = forms.BooleanField(required=False, label="Email me when people RSVP")
    copy_me = forms.BooleanField(required=False, label="Send me a copy of the invitation")
    
    def save(self, *args, **kwargs):
        guest_invites = []
        event = self.instance.content_object
        rsvp_notification = self.cleaned_data["rsvp_notification"]
        for email in self.cleaned_data["emails"]:
            guest, created = Guest.objects.get_or_create(event=event, email=email, 
                defaults={"invited":datetime.date.today()})
            guest.notify_on_rsvp = rsvp_notification
            guest.save()
            guest_invites.append(guest)
        if self.cleaned_data["copy_me"]:
            self.cleaned_data["emails"].append(self.instance.user.email)
        super(GuestInviteForm, self).save(*args, **kwargs)
        return guest_invites

class GuestAddForm(forms.ModelForm):
    first_name = forms.CharField(required=True, max_length=50)
    zipcode = forms.CharField(max_length=5, min_length=5, required=False)
    rsvp_status = forms.ChoiceField(choices=Guest.RSVP_STATUSES, 
        label="Is this person planning on attending?", widget=forms.RadioSelect)
        
    class Meta:
        model = Guest
        fields = ("first_name", "last_name", "email", "phone", "zipcode", "rsvp_status",)
        widgets = {
            "rsvp_status": forms.RadioSelect,
        }
        
    def clean_email(self):
        data = self.cleaned_data["email"]
        if data and Guest.objects.filter(event=self.instance.event, email=data).exists():
            raise forms.ValidationError("A Guest with this email address already exists.")
        return data
            
    def clean_zipcode(self):
        data = self.cleaned_data["zipcode"]
        if data:
            try:
                self.cleaned_data["location"] = Location.objects.get(zipcode=data)
            except Location.DoesNotExist:
                raise forms.ValidationError("Invalid zipcode %s" % data)
        return data
        
    def save(self, *args, **kwargs):
        self.instance.added = datetime.date.today()
        return super(GuestAddForm, self).save(*args, **kwargs)
        
class GuestListForm(forms.Form):
    from actions import attending, not_attending, announcement_email, invitation_email, \
        reminder_email, remove, make_host, unmake_host
    ACTIONS = {
        "1_SA": ("Mark as Attending", attending),
        "2_SN": ("Mark as Not Attending", not_attending),
        "3_EA": ("Send Announcement Email", announcement_email),
        "4_EI": ("Send Invitation Email", invitation_email),
        "5_ER": ("Send Reminder Email", reminder_email),
        "6_MR": ("Remove from guest list", remove),
        "7_MH": ("Make a guest a host", make_host),
        "8_MU": ("Remove host privledges", unmake_host),
    }
    ACTION_CHOICES = [("", "- Select One -")] + sorted([(k, v[0]) for k,v in ACTIONS.iteritems()])
    
    action = forms.ChoiceField(choices=ACTION_CHOICES)
    guests = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, event, *args, **kwargs):
        super(GuestListForm, self).__init__(*args, **kwargs)
        self.event = event
        self.fields["guests"].queryset = event.guest_set.all()
        
    def clean(self):
        action = self.cleaned_data.get("action", "")
        if re.search("^\d+_E", action): # Check to see if the action is of type Email
            if any([not g.email for g in self.cleaned_data["guests"]]): # Action of type Email can only be performed on guests with emails
                raise forms.ValidationError("All guests must have an email address")
        return self.cleaned_data
        
    def save(self, *args, **kwargs):
        action = GuestListForm.ACTIONS[self.cleaned_data["action"]][1]
        return action(self.cleaned_data["guests"])
        
class GuestEditForm(forms.ModelForm):
    name = forms.CharField(required=False, max_length=100)
    zipcode = forms.CharField(required=False, max_length=5)
    
    class Meta:
        model = Guest
        
    def clean_zipcode(self):
        data = self.cleaned_data["zipcode"]
        if data:
            try:
                self.cleaned_data["location"] = Location.objects.get(zipcode=data)
            except Location.DoesNotExist:
                raise forms.ValidationError("Invalid zipcode %s" % data)
        return data
        
    def save(self, *args, **kwargs):
        name = self.cleaned_data.get("name", None)
        if name:
            self.instance.name = name
        zipcode = self.cleaned_data.get("zipcode", None)
        if zipcode:
            self.instance.zipcode = zipcode
        return super(GuestEditForm, self).save(*args, **kwargs)
        
class RsvpForm(forms.ModelForm):
    rsvp_status = forms.ChoiceField(choices=Guest.RSVP_STATUSES, widget=forms.RadioSelect)
    token = forms.CharField(required=False, widget=forms.HiddenInput)
    
    class Meta:
        model = Guest
        fields = ("rsvp_status", "comments", "token",)
        widgets = {
            "comments": forms.Textarea(attrs={"cols": "17"})
        }
        
    def clean_token(self):
        data = self.cleaned_data["token"]
        event = self.instance.event
        if event.is_private and not event.is_token_valid(data):
            return forms.ValidationError("Invalid token")
        return data

    def save(self, request, *args, **kwargs):
        guest = super(RsvpForm, self).save(*args, **kwargs)
        guest.event.save_guest_in_session(request=request, guest=guest)
        rsvp_recieved.send(sender=self, guest=guest)
        return guest

class RsvpConfirmForm(forms.ModelForm):
    first_name = forms.CharField(required=True, max_length=50)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Guest
        fields = ("first_name", "last_name", "email", "phone",)
        
    def save(self, request, *args, **kwargs):
        guest = super(RsvpConfirmForm, self).save(*args, **kwargs)
        guest.event.save_guest_in_session(request=request, guest=guest)
        return guest
        
class RsvpAccountForm(forms.ModelForm):
    zipcode = forms.CharField(max_length=10, required=False)
    password1 = forms.CharField(label='Password', min_length=5, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = Guest
        fields = ("zipcode", "password1", "password2",)
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        if len(password2) < 5:
            raise forms.ValidationError("Your password must contain at least 5 characters.")
        return password2
        
    def clean_zipcode(self):
        data = self.cleaned_data['zipcode'].strip()
        if not len(data):
            self.instance.location = None
            return
        if len(data) <> 5:
            raise forms.ValidationError("Please enter a 5 digit zipcode")
        try:
            self.cleaned_data["location"] = Location.objects.get(zipcode=data)
        except Location.DoesNotExist, e:
            raise forms.ValidationError("Zipcode is invalid")
            
    def save(self, request, *args, **kwargs):
        user = User(first_name=self.instance.first_name, last_name=self.instance.last_name, 
            email=self.instance.email)
        user.username = hashlib.md5(self.instance.email).hexdigest()[:30]
        user.set_password(self.cleaned_data.get("password1", auth.models.UNUSABLE_PASSWORD))
        user.save()
        self.instance.user = user
        template = loader.get_template("rah/registration_email.html")
        context = {"user": user, "domain": Site.objects.get_current().domain,}
        msg = EmailMessage("Registration", template.render(Context(context)), None, [user.email])
        msg.content_subtype = "html"
        msg.send()
        guest = super(RsvpAccountForm, self).save(*args, **kwargs)
        guest.event.save_guest_in_session(request=request, guest=guest)
        return guest
        
class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        exclude = ("name", "event_type", "is_active",)
        
    def __init__(self, guest, *args, **kwargs):
        self.guest = guest
        super(SurveyForm, self).__init__(*args, **kwargs)
        for challenge in self.instance.challenge_set.order_by("order"):
            self.fields[challenge.name] = forms.ChoiceField(choices=Commitment.ANSWERS, 
                widget=forms.RadioSelect, required=False)
            try:
                commitment = Commitment.objects.get(guest=self.guest, challenge=challenge)
                self.fields[challenge.name].initial = commitment.answer
            except Commitment.DoesNotExist:
                pass
                
    def save(self, *args, **kwargs):
        for key,data in self.cleaned_data.items():
            if data:
                challenge = self.instance.challenge_set.get(name=key)
                commitment, created = Commitment.objects.get_or_create(guest=self.guest, challenge=challenge)
                commitment.answer = data
                commitment.save()
        return self.instance