import datetime
import hashlib
import re

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template import Context, loader

from geo.models import Location
from invite.models import Invitation
from invite.forms import InviteForm
from invite.fields import MultiEmailField

from models import Event, Guest

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

class EventForm(forms.ModelForm):
    city = forms.CharField(required=False, max_length=50)
    state = forms.ChoiceField(required=False, choices=[("", "state")]+[(state, state) for state in STATES])
    zipcode = forms.CharField(required=False, max_length=5)
    is_private = forms.ChoiceField(choices=((True, "Yes"), (False, "No")), initial=False,
        widget=forms.RadioSelect)
    
    class Meta:
        model = Event
        fields = ["event_type", "where", "city", "state", "zipcode", "when", "start", "end", 
            "details", "is_private"]
        widgets = {
            "event_type": forms.RadioSelect,
            "when": forms.TextInput(attrs={"class": "datepicker"}),
            "start": forms.Select(choices=[("", "start")]+TIMES),
            "end": forms.Select(choices=[("", "end")]+TIMES),
        }
        
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if self.instance.location:
            self.fields["city"].initial = self.instance.location.name
            self.fields["state"].initial = self.instance.location.st
            self.fields["zipcode"].initial = self.instance.location.zipcode
        
    def clean_zipcode(self):
        data = self.cleaned_data["zipcode"]
        if data:
            try:
                self.cleaned_data["location"] = Location.objects.get(zipcode=data)
            except Location.DoesNotExist:
                raise forms.ValidationError("Invalid zipcode %s" % data)
        return data
        
    def clean_when(self):
        data = self.cleaned_data["when"]
        if (data - datetime.date.today()).days < 0:
            raise forms.ValidationError("Event must occur in the future.")
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
        
    def save(self, user, *args, **kwargs):
        self.instance.creator = user
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
            guest_invites.append(Guest.objects.create(event=event, email=email, 
                invited=datetime.date.today(), notify_on_rsvp=rsvp_notification))
        if self.cleaned_data["copy_me"]:
            self.cleaned_data["emails"].append(self.instance.user.email)
        super(GuestInviteForm, self).save(*args, **kwargs)
        return guest_invites

class GuestAddForm(forms.ModelForm):
    is_attending = forms.ChoiceField(choices=(("A", "Yes"), ("N", "No")),
        widget=forms.RadioSelect, label="Is this person planning on attending?", required=False)
        
    class Meta:
        model = Guest
        fields = ("first_name", "last_name", "email", "phone", "is_attending",)
        
    def clean_is_attending(self):
        data = self.cleaned_data["is_attending"]
        self.instance.rsvp_status = data
        return data
        
    def save(self, *args, **kwargs):
        self.instance.added = datetime.date.today()
        super(GuestAddForm, self).save(*args, **kwargs)
        
class GuestListForm(forms.Form):
    from actions import attending, not_attending, invitation_email, remove, make_host, unmake_host
    ACTIONS = {
        "1_SA": ("Mark as Attending", attending),
        "2_SN": ("Mark as Not Attending", not_attending),
        "3_EI": ("Send Invitation Email", invitation_email),
        "3_MR": ("Remove from guest list", remove),
        "4_MH": ("Make a guest a host", make_host),
        "5_MU": ("Remove host privledges", unmake_host),
    }
    ACTION_CHOICES = [("", "- Select One -")] + sorted([(k, v[0]) for k,v in ACTIONS.iteritems()])
    
    action = forms.ChoiceField(choices=ACTION_CHOICES)
    guests = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, event, *args, **kwargs):
        super(GuestListForm, self).__init__(*args, **kwargs)
        self.event = event
        self.fields["guests"].queryset = event.guest_set.all()
        
    def clean(self):
        if re.search("^\d+_E", self.cleaned_data.get("action", "")): # Check to see if the action is of type Email
            if any([not g.email for g in self.cleaned_data["guests"]]): # Action of type Email can only be performed on guests with emails
                raise forms.ValidationError("All guests must have an email address")
        return self.cleaned_data
        
    def save(self, *args, **kwargs):
        action = GuestListForm.ACTIONS[self.cleaned_data["action"]][1]
        return action(self.cleaned_data["guests"])
        
class RsvpForm(forms.ModelForm):
    rsvp_status = forms.ChoiceField(choices=Guest.RSVP_STATUSES, widget=forms.RadioSelect)
    token = forms.CharField(required=False, widget=forms.HiddenInput)
    
    class Meta:
        model = Guest
        fields = ("rsvp_status", "token",)
        
    def clean_token(self):
        data = self.cleaned_data["token"]
        event = self.instance.event
        if event.is_private and not event.is_token_valid(data):
            return forms.ValidationError("Invalid token")
        return data

    def save(self, request, *args, **kwargs):
        guest = super(RsvpForm, self).save(*args, **kwargs)
        guest.event.save_guest_in_session(request=request, guest=guest)
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