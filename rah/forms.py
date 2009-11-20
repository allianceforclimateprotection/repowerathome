from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    """
        Extends the stock User Creation Form that ships with auth to include an email field
    """
    email = forms.EmailField(label=_("Email"))
    
    class Meta:
        model = User
        fields = ("username","email")