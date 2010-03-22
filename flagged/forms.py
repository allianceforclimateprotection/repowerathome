from django import forms

from models import Flag

class FlagForm(forms.ModelForm):
    class Meta:
        model = Flag
        fields = ("content_type", "object_pk")
        widgets = {
            "content_type": forms.HiddenInput,
            "object_pk": forms.HiddenInput,
        }