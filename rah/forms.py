from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from www.rah.models import Signup, Profile, Location, ActionStatus

class RegistrationForm(UserCreationForm):
    """
        Extends the stock User Creation Form that ships with auth to include an email field
    """
    email = forms.EmailField(label="Email")
    
    class Meta:
        model = User
        fields = ("username","email",)

class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ("email","zipcode",)

    def clean_zipcode(self):
        data = self.cleaned_data['zipcode']
        if (not data.isdigit()) or (len(data) <> 5):
            raise forms.ValidationError("Please enter a valid 5 digit zipcode")

        return data

class InquiryForm(forms.ModelForm):
    zipcode = forms.CharField(max_length=5)
    
    class Meta:
        model = Profile
        fields = ("zipcode", "building_type")
        
    def clean_zipcode(self):
        data = self.cleaned_data['zipcode']
        # TODO Remove debug print statements before commiting 
        print "Data: %s" % (data)
        if len(data) <> 5:
            raise forms.ValidationError("Please enter a 5 digit zipcode")
        try:
            self.instance.location = Location.objects.get(zipcode=data)
        except Location.DoesNotExist, e:
            raise forms.ValidationError("Zipcode is invalid")

class ActionStatusForm(forms.ModelForm):
    class Meta:
        model = ActionStatus
        fields = ("status",)