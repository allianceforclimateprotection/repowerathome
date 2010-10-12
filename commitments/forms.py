from django import forms
from django.forms import ModelForm

from models import Contributor
from geo.models import Location

class ContributorForm(forms.ModelForm):
    
    zipcode = forms.CharField(max_length=10, required=False, help_text="Leave blank if not a US resident")
    email = forms.EmailField(label='Email', widget=forms.TextInput, required=False)
    first_name = forms.CharField(min_length=2)
    
    class Meta:
        model = Contributor
        fields = ('first_name', 'last_name', 'email', 'phone')
        
    def clean(self):
        email = self.cleaned_data.get('email', None)
                
        # If there's an email we'll try to match it to contributors in the data. If there's already a contributor id
        # then we can skip the lookup because we're editing a known contributor
        if email and not self.instance.id:
            try:
                self.instance = Contributor.objects.get(email=email)
            except Contributor.DoesNotExist:
                # We didn't match this email to an existing contributor, so we're going to make a new one
                pass
            else:
                # We don't want to delete any fields that may exist in the database
                for key in self.cleaned_data.keys():
                    if self.cleaned_data.get(key) == '':
                        del(self.cleaned_data[key])
        
        return self.cleaned_data
    
    def clean_email(self):
        # If there is no email entered, make sure it's set to NULL in the DB because there can't be more than one ''
        email = self.cleaned_data.get('email')
        if email == '':
            self.cleaned_data['email'] = None
        
        return self.cleaned_data['email']
        
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