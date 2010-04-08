from django import forms

from records.models import Record

from models import UserActionProgress

class BaseActionForm(forms.Form):
    def __init__(self, user, action, *args, **kwargs):
        super(BaseActionForm, self).__init__(*args, **kwargs)
        self.user = user
        self.action = action

class ActionCommitForm(BaseActionForm):
    date_committed = forms.DateField(label="Commit date",
        widget=forms.DateInput(attrs={"class": "date_commit_field"}))
        
    def save(self):
        self.action.commit_for_user(self.user, self.cleaned_data["date_committed"])