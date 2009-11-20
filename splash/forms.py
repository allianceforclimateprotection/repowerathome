from django import forms
from www.splash.models import Signup

class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ("email","zipcode")
    
    def clean_zipcode(self):
        data = self.cleaned_data['zipcode']
        if not data.isdigit() or len(data) < 5 or len(data) > 5:
            raise forms.ValidationError("Please enter a valid 5 digit zipcode")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data
