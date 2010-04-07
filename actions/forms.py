from django import forms

from records.models import Record

from models import UserActionProgress

class BaseActionForm(forms.Form):
    def __init__(self, user, action, *args, **kwargs):
        super(BaseActionForm, self).__init__(*args, **kwargs)
        self.user = user
        self.action = action

class ActionCompleteForm(BaseActionForm):
    def save(self):
        uap, c = UserActionProgress.objects.get_or_create(user=self.user, action=self.action)
        was_completed = uap.is_completed
        uap.is_completed = True
        uap.save()
        if not was_completed:
            Record.objects.create_record(self.user, "action_complete", self.action)

class ActionUndoForm(BaseActionForm):
    def save(self):
        try:
            uap = UserActionProgress.objects.get(user=self.user, action=self.action)
            uap.is_completed = False
            uap.save()
        except UserActionProgress.DoesNotExisit:
            pass

class ActionCommitForm(BaseActionForm):
    date_committed = forms.DateField(label="Commit date",
        widget=forms.DateInput(attrs={"class": "date_commit_field"}))
        
    def save(self):
        uap, c = UserActionProgress.objects.get_or_create(user=self.user, action=self.action)
        was_committed = uap.date_committed != None
        uap.date_committed = self.cleaned_data["date_committed"]
        uap.save()
        if not was_committed:
            Record.objects.create_record(self.user, "action_commitment", self.action, 
                data={"date_committed": uap.date_committed})