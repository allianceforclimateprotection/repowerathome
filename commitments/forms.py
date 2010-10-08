from django import forms
from django.forms import ModelForm

from models import Contributor

class ContributorForm(forms.ModelForm):
    
    zipcode = forms.CharField(max_length=10, required=False, help_text="Leave blank if not a US resident")
    # email = forms.EmailField(label='Email', widget=forms.TextInput)
    first_name = forms.CharField(min_length=2)
    
    class Meta:
        model = Contributor
        fields = ('first_name', 'last_name', 'email', 'phone')
    
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
        