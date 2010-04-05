from django import forms

class ActionCommitForm(forms.Form):
    date_committed = forms.DateField(label="Commit date", required=False)
    cancel_commitment = forms.BooleanField(required=False)
    
    def save(self, action, user):
        date = None if self.cleaned_data['cancel_commitment'] else self.cleaned_data['date_committed']
        user.set_action_commitment(action, date)