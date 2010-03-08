from django import forms
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User

from geo.models import Location

from models import Group, GroupUsers
from fields import UserModelMultipleChoiceField

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