from django import forms
from smtplib import SMTPException

from django.contrib.sites.models import Site
from django.core.mail import send_mail, EmailMessage
from django.template import Context, loader
from django.contrib import messages

from utils import hash_val
from models import Invitation
        
class InviteForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea, label="Personal note (optional)", required=False)
    signature = forms.CharField(widget=forms.HiddenInput)
    
    class Meta:
        model = Invitation
        fields = ("email", "note", "token", "content_type", "object_pk")
        widgets = {
            "token": forms.HiddenInput,
            "content_type": forms.HiddenInput,
            "object_pk": forms.HiddenInput,
        }
    
    def __init__(self, *args, **kwargs):
        form = super(InviteForm, self).__init__(*args, **kwargs)
        self.fields["signature"].initial = hash_val((self.instance.content_type, self.instance.object_pk,))
        
    def clean(self):
        content_type = self.cleaned_data["content_type"]
        object_pk = self.cleaned_data["object_pk"]
        if content_type or object_pk:
            try:
                target = content_type.get_object_for_this_type(pk=object_pk)
            except ObjectDoesNotExist:
                raise forms.ValidationError("No object found matching %s" % object_pk)
            except ValueError:
                raise forms.ValidationError("Invalid parameters %s, %s" % (content_type_pk, object_pk))
            if hash_val((content_type, object_pk,)) != self.cleaned_data["signature"]:
                raise forms.ValidationError("Signature has been currupted")
        return self.cleaned_data
    
    def save(self):
        invite = super(InviteForm, self).save()
        ct = self.instance.content_type
        template_list = ["invite/invite.html",]
        if ct:
            template_list = [
                "invite/%s/%s/invite.html" % (ct.model_class()._meta.app_label, ct.model_class()._meta.module_name),
                "invite/%s/invite.html" % ct.model_class()._meta.app_label,
            ] + template_list
        context = {"from_user": invite.user, "note": self.cleaned_data["note"], "invite": invite,
            "domain": Site.objects.get_current().domain,}
        msg = EmailMessage("Invitation from %s to Repower at Home" % invite.user.get_full_name(),
            loader.render_to_string(template_list, context), None, [invite.email])
        msg.content_subtype = "html"
        try:
            msg.send()
        except SMTPException, e:
            return False    
        return invite
