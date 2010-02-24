from django import forms
from django.core.urlresolvers import resolve, reverse

from models import Group

class GroupForm(forms.ModelForm):
    name = forms.CharField(label="Group name", help_text="Enter a name for your new group")
    slug = forms.SlugField(label="Group address", help_text="This will be your group's web address")
    description = forms.CharField(label="Group description", help_text="What is the group all about?", widget=forms.Textarea)
    image = forms.FileField(label="Upload a group image", help_text="You can upload png, jpg or gif files upto 512K", required=False)
    
    group_name_blacklist = ["user", "users", "admin",]
    
    class Meta:
        model = Group
        exclude = ("is_featured", "users", "requesters",)
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
        try:
            if data in GroupForm.group_name_blacklist or resolve(reverse("group_detail", args=[data]))[0].__name__ != "group_detail":
                raise forms.ValidationError("This Group address is not allowed.")
        except:
            raise forms.ValidationError("This Group address is not allowed.")
        return data