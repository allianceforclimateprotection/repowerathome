from django import forms

from models import Rating
from widgets import IsHelpfulWidget

class RatingForm(forms.ModelForm):
    score = forms.IntegerField(label="", widget=IsHelpfulWidget)
    
    class Meta:
        model = Rating
        fields = ("content_type", "object_pk", "score")
        widgets = {
            "content_type": forms.HiddenInput,
            "object_pk": forms.HiddenInput,
        }