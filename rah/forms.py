from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from www.rah.models import *
from django.forms import ValidationError
from django.core.urlresolvers import resolve, Resolver404
from urlparse import urlparse
from django.forms.widgets import CheckboxSelectMultiple

class RegistrationForm(UserCreationForm):
    """
        Extends the stock User Creation Form that ships with auth to include an email field
    """
    email = forms.EmailField(label="Email")
    
    class Meta:
        model = User
        fields = ("username","email",)

    def clean_username(self):
        """
            Ensures that any usernames added will not conflict with exisiting commands
        """
        username = super(RegistrationForm, self).clean_username()
        valid = False
        try:
            view_function = resolve(urlparse('/' + username + '/')[2])[0]
            if view_function.func_name == 'profile':
                valid = True
        except Resolver404, re:
            #TODO: create a list of urls we want to save; then validate the username against these
            valid = True
        except AttributeError, ae:
            pass
            
        if not valid:
            raise ValidationError('This username has been reserved by our system.  Please choose another.')
        return username

class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ("email","zipcode",)

    def clean_zipcode(self):
        data = self.cleaned_data['zipcode']
        if (not data.isdigit()) or (len(data) <> 5):
            raise forms.ValidationError("Please enter a valid 5 digit zipcode")

        return data

class ProfileEditForm(forms.ModelForm):
    zipcode = forms.CharField(max_length=5, required=False)
    
    class Meta:
        model = Profile
        fields = ("zipcode", "building_type")
        
    def clean_zipcode(self):
        data = self.cleaned_data['zipcode'].strip()
        # TODO Remove debug print statements before commiting 
        if len(data) == 0:
            return
        if len(data) <> 5:
            raise forms.ValidationError("Please enter a 5 digit zipcode")
        try:
            self.instance.location = Location.objects.get(zipcode=data)
        except Location.DoesNotExist, e:
            raise forms.ValidationError("Zipcode is invalid")

class UserActionTaskForm(forms.Form):
    is_done = forms.BooleanField(label='test')
    
    class Meta:
        model = UserActionTask
        fields = ("is_done",)

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

class AccountForm(forms.ModelForm):
    """docstring for AccountForm"""
    class Meta:
        model = User
        fields = ('email',)
        