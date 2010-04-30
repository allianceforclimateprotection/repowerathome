from django import forms
from smtplib import SMTPException

from django.contrib.sites.models import Site
from django.core.mail import send_mail, EmailMessage
from django.template import Context, loader
from django.contrib import messages

from utils import hash_val
from models import Invitation

class InviteForm(forms.Form):
    to_email = forms.EmailField(min_length=5, max_length=255, label="Email to")
    note = forms.CharField(widget=forms.Textarea, label="Personal note (optional)", required=False)
    invite_type = forms.CharField(widget=forms.HiddenInput, required=False, initial='default')
    content_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content_id_sig = forms.CharField(widget=forms.HiddenInput, required=False)
    
    def __init__(self, *args, **kwargs):
        super(InviteForm, self).__init__(*args, **kwargs)
        # If a content_id or invite_type was passed in, sign it
        if 'invite_type' in self.initial or 'content_id' in self.initial:
            self.fields['content_id_sig'].initial = hash_val((self.initial.get('invite_type'), self.initial.get('content_id'),))
    
    def clean_content_id(self):
        """Verify the content_id_sig"""
        content_id = self.cleaned_data['content_id']
        sig_check = hash_val((self.data['invite_type'], content_id,))
        if content_id and sig_check <> self.data['content_id_sig']:
            raise forms.ValidationError('Content ID is currupted')
        return content_id
    
    def save(self, from_user):
        to_email    = self.cleaned_data['to_email']
        invite_type = self.cleaned_data['invite_type']
        content_id  = self.cleaned_data['content_id']
        invite = Invitation.objects.invite(from_user, to_email, invite_type, content_id)
        template = loader.get_template('emails/%s.html' % invite_type)
        context = { 'from_user': from_user, 'note': self.cleaned_data['note'], 
            "invite": invite, "domain": Site.objects.get_current().domain, }
        msg = EmailMessage('Invitation from %s to Repower at Home' % from_user.get_full_name(),
                template.render(Context(context)), None, [to_email])
        msg.content_subtype = "html"
        try:
            msg.send()
        except SMTPException, e:
            return False
        return True