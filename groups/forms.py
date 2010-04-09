import os

from django import forms
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User

from PIL.Image import open as pil_open

from geo.models import Location

from models import Group, GroupUsers, Discussion

class GroupForm(forms.ModelForm):
    IMAGE_FORMATS = {"PNG": "png", "JPEG": "jpeg", "GIF": "gif"}
    
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
        exclude = ("is_featured", "is_geo_group", "location_type", "sample_location", 
                   "parent", "users", "requesters", "email_blacklisted", "disc_moderation", "disc_post_perm",)
        widgets = {
            "membership_type": forms.RadioSelect
        }
        
    def clean_image(self):
        data = self.cleaned_data["image"]
        if data:
            if data.size > 4194304:
                raise forms.ValidationError("Group images can not be larger than 512K")
            self.image_format = pil_open(data.file).format
            if not self.image_format in GroupForm.IMAGE_FORMATS:
                raise forms.ValidationError("Images can not be of type %s" % data.content_type)
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
        
    def save(self):
        group = super(GroupForm, self).save()
        if group.image:
            image_name = "%s.%s" % (group.pk, GroupForm.IMAGE_FORMATS[self.image_format])
            original = group.image.file
            group.image.save(image_name, original, save=True)
            os.remove(original.name)
        return group
        
class MembershipForm(forms.Form):
    MEMBERSHIP_ROLES = (
        ('', '--Set Membership Role--'),
        ('M', 'Manager',),
        ('N', 'Regular Member',),
        ('D', 'Remove from Group',),
    )
    role = forms.ChoiceField(label="", choices=MEMBERSHIP_ROLES, error_messages={"required": "You must select a membership action."})
    memberships = forms.ModelMultipleChoiceField(queryset=GroupUsers.objects.all(), widget=forms.CheckboxSelectMultiple,
        error_messages={"required": "You must select at least one member from the group."})
    
    def __init__(self, group, *args, **kwargs):
        super(MembershipForm, self).__init__(*args, **kwargs)
        self.group = group
        self.fields["memberships"].queryset = GroupUsers.objects.filter(group=group)
        
    def clean(self):
        data = self.cleaned_data
        role = data["role"] if "role" in data else ""
        memberships = data["memberships"] if "memberships" in data else []
        if (role == "N" or role == "D") and self.group.number_of_managers() == len(memberships):
            self._errors["memberships"] = forms.util.ErrorList(["You must leave at least one manager in the group."])
            del self.cleaned_data["memberships"]
        return self.cleaned_data
        
    def save(self):
        role = self.cleaned_data["role"]
        memberships = self.cleaned_data["memberships"]
        if role == "M":
            memberships.update(is_manager=True)
        elif role == "N":
            memberships.update(is_manager=False)
        elif role == "D":
            memberships.delete()
        else:
            raise NameError("Role option %s does not exist" % role)

class DiscussionSettingsForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("disc_moderation", "disc_post_perm", )
        widgets = {
            "disc_moderation": forms.RadioSelect,
            "disc_post_perm": forms.RadioSelect
        }

class DiscussionCreate(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ("subject", "body",)
