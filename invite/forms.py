from django import forms
from smtplib import SMTPException
from django.core.mail import send_mail, EmailMessage
from django.template import Context, loader
from django.contrib import messages
from utils import hash_val
from models import Invitation

class InviteForm(forms.Form):
    to_email = forms.EmailField(min_length=5, max_length=255, label="To email")
    note = forms.CharField(widget=forms.Textarea, label="Personal note (optional)", required=False)
    content_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content_id_sig = forms.CharField(widget=forms.HiddenInput, required=False)
    
    def clean_content_id(self):
        content_id = self.cleaned_data['content_id']
        if content_id and hash_val(content_id) <> self.data['content_id_sig']:
            raise forms.ValidationError('Content ID is currupted')
        return content_id
    
    def save(self, from_user, invite_type="default"):
        invite = Invitation.objects.invite(from_user, self.cleaned_data['to_email'], invite_type, self.cleaned_data['content_id'])
        template = loader.get_template('emails/%s.html' % invite_type)
        context = { 'from_user': from_user, 'note': self.cleaned_data['note'], "invite": invite }
        try:
            send_mail(
                'Invitation from %s to Repower@Home' % from_user.get_full_name(), 
                template.render(Context(context)),
                None, 
                [self.cleaned_data['to_email']], 
                fail_silently=False
            )
        except SMTPException, e:
            return False
        return True