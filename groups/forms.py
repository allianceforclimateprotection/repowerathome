from django import forms
from django.core.urlresolvers import resolve, reverse

from geo.models import Location

from models import Group

class GroupForm(forms.ModelForm):
    name = forms.CharField(label="Group name", help_text="Enter a name for your new group")
    slug = forms.SlugField(label="Group address", help_text="This will be your group's web address")
    description = forms.CharField(label="Group description", help_text="What is the group all about?", widget=forms.Textarea)
    image = forms.FileField(label="Upload a group image", help_text="You can upload png, jpg or gif files upto 512K", required=False)

    states = ["ak", "al", "ar", "az", "ca", "co", "ct", "dc", "de", "fl", "ga", "hi", "ia", "id", "il", 
        "in", "ks", "ky", "la", "ma", "md", "me", "mi", "mn", "mo", "ms", "mt", "nc", "nd", "ne", 
        "nh", "nj", "nm", "nv", "ny", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", 
        "va", "vt", "wa", "wi", "wv", "wy"]
    group_name_blacklist = ["user", "users", "admin",]
    
    class Meta:
        model = Group
        exclude = ("is_featured", "is_geo_group", "location_type", "sample_location", "parent", "users", "requesters",)
        widgets = {
            "membership_type": forms.RadioSelect
        }
        
    def clean_image(self):
        data = self.cleaned_data["image"]
        if data and data.size > 4194304:
            raise forms.ValidationError("Group images can not be larger than 512K")
        return data
        
    def clean_slug(self):
        data = self.cleaned_data["slug"]
        if data in GroupForm.states or any([data.startswith("%s-" % state) for state in GroupForm.states]):
            raise forms.ValidationError("Group addresses can not begin with a state name.")
        try:
            if data in GroupForm.group_name_blacklist or resolve(reverse("group_detail", args=[data]))[0].__name__ != "group_detail":
                raise forms.ValidationError("This Group address is not allowed.")
        except:
            raise forms.ValidationError("This Group address is not allowed.")
        return data