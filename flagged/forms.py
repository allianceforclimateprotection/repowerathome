from django import forms

from models import Flag

class FlagForm(forms.ModelForm):
    flagged = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "button"}))
    
    def __init__(self, *args, **kwargs):
        super(FlagForm, self).__init__(*args, **kwargs)
        self.id = "%s_%s" % (self.instance.content_type.pk, self.instance.object_pk)
        if self.instance.submit_date: self.fields["flagged"].initial = True
    
    class Meta:
        model = Flag
        fields = ("flagged", "content_type", "object_pk")
        widgets = {
            "content_type": forms.HiddenInput,
            "object_pk": forms.HiddenInput,
        }