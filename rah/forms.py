from django import forms
from django.contrib import auth
from rah.models import *
from django.forms import ValidationError
from django.core.mail import send_mail, EmailMessage
from django.core.urlresolvers import resolve, Resolver404
from urlparse import urlparse
from django.forms.widgets import CheckboxSelectMultiple
from smtplib import SMTPException
from django.template import Context, loader
import hashlib

import settings

class RegistrationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and password.
    """
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email",)

    def clean(self):
        self.instance.username = hashlib.md5(self.cleaned_data.get("email", "")).hexdigest()[:30] 
        self.instance.set_password(self.cleaned_data.get("password1", auth.models.UNUSABLE_PASSWORD))
        super(RegistrationForm, self).clean()        
        return self.cleaned_data

    def clean_email(self):
        """
        Ensure that the email address is valid and unique
        """
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address has already been registered in our system. If you have forgotten your password, please use the password reset link.')
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        if len(password2) < 5:
            raise forms.ValidationError("Your password must contain at least 5 characters.")
        return password2

class AuthenticationForm(forms.Form):
   """
   Base class for authenticating users. Extend this to get a form that accepts
   username/password logins.
   """
   email = forms.EmailField(label="Email")
   password = forms.CharField(label="Password", widget=forms.PasswordInput)

   def __init__(self, request=None, *args, **kwargs):
       """
       If request is passed in, the form will validate that cookies are
       enabled. Note that the request (a HttpRequest object) must have set a
       cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
       running this validation.
       """
       self.request = request
       self.user_cache = None
       super(AuthenticationForm, self).__init__(*args, **kwargs)

   def clean(self):
       email = self.cleaned_data.get('email')
       password = self.cleaned_data.get('password')

       if email and password:
           self.user_cache = auth.authenticate(username=email, password=password)
           if self.user_cache is None:
               # FIXME: email should not be case sensitive
               raise forms.ValidationError("Please enter a correct email and password. Note that both fields are case-sensitive.")
           elif not self.user_cache.is_active:
               raise forms.ValidationError("This account is inactive.")

       # TODO: determine whether this should move to its own method.
       if self.request:
           if not self.request.session.test_cookie_worked():
               raise forms.ValidationError("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in.")

       return self.cleaned_data

   def get_user_id(self):
       if self.user_cache:
           return self.user_cache.id
       return None

   def get_user(self):
       return self.user_cache

class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ("email","zipcode",)

    def clean_zipcode(self):
        data = self.cleaned_data['zipcode']
        if (not data.isdigit()) or (len(data) <> 5):
            raise forms.ValidationError("Please enter a valid 5 digit zipcode")

        return data

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("comment", "beta_group", "url")
    
    url = forms.CharField(widget=forms.HiddenInput, required=False)
    comment = forms.CharField(widget=forms.Textarea, required=False, label="Your Comments")
    beta_group = forms.BooleanField(help_text="""Check here if you would like to be a part 
                                                of our alpha group and receive information 
                                                on new features before they launch.""", label="", required=False)
    def send(self, user):
        template = loader.get_template('rah/feedback_email.html')
        context  = { 'feedback': self.cleaned_data, 'user': user, }
        msg = EmailMessage('Feedback Form', template.render(Context(context)), None, ["feedback@repowerathome.com"])
        msg.content_subtype = "html"
        msg.send()
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("zipcode", "building_type", "is_profile_private")
        
    zipcode = forms.CharField(max_length=5, required=False)
    is_profile_private = forms.BooleanField(label="Make Profile Private", required=False)
    
    def clean_zipcode(self):
        data = self.cleaned_data['zipcode'].strip()
        if not len(data):
            self.instance.location = None
            return
        if len(data) <> 5:
            raise forms.ValidationError("Please enter a 5 digit zipcode")
        try:
            self.instance.location = Location.objects.get(zipcode=data)
        except Location.DoesNotExist, e:
            raise forms.ValidationError("Zipcode is invalid")

class AccountForm(forms.ModelForm):
    """docstring for AccountForm"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not len(email):
            raise ValidationError('Email can not be blank')

        if self.instance.email == email or self.instance.set_email(email):
            return email
        else:
             raise ValidationError('This email address has already been registered in our system.')

class ActionAdminForm(forms.ModelForm):
    class Meta:
        model = Action
    
    #OPTIMIZE: make function reusable by creating an abstract sluggable form
    def clean_slug(self):
        import re
        data = self.cleaned_data['slug']
        
        if not re.search('^[a-z0-9-]+$', data):
            raise forms.ValidationError("Slugs can only contain lowercase letters a-z, number 0-9, and a hyphen")
    
        return data

class ActionCatAdminForm(forms.ModelForm):
    class Meta:
        model = ActionCat

    def clean_slug(self):
        import re
        data = self.cleaned_data['slug']

        if not re.search('^[a-z0-9-]+$', data):
            raise forms.ValidationError("Slugs can only contain lowercase letters a-z, number 0-9, and a hyphen")

        return data
        
class HousePartyForm(forms.Form):
    phone_number = forms.CharField()
    call_time = forms.ChoiceField(choices=(('anytime', 'Anytime'), ('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening')))
    
    def send(self, user):
        template = loader.get_template('rah/house_party_email.html')
        context = {
            'name': user.get_full_name(),
            'email': user.email,
            'call_time': self.cleaned_data['call_time'],
            'phone_number': self.cleaned_data['phone_number'],
        }
        try:
            send_mail('House Party Contact', template.render(Context(context)), None, 
                ["feedback@repowerathome.com"], fail_silently=False)
        except SMTPException, e:
            return False
        return True

class InviteFriendForm(forms.Form):
    to_email = forms.EmailField(min_length=5, max_length=255, label="To email")
    note = forms.CharField(widget=forms.Textarea, label="Personal note (optional)", required=False)
        
    def send(self, from_user):
        template = loader.get_template('rah/invite_friend_email.html')
        context = { 'from_user': from_user, 'note': self.cleaned_data['note'] }
        try:
            send_mail(
                'Invitation from %s to Repower@Home' % from_user.get_full_name(), 
                template.render(Context(context)),
                None, 
                [self.cleaned_data['to_email']], 
                fail_silently=False
            )
        except SMTPException, e:
            return False
        return True