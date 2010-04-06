from django import forms

from records.models import Record

from models import UserActionProgress

class ActionForm(forms.Form):
    date_committed = forms.DateField(label="Commit date", required=False,
        widget=forms.DateInput(attrs={"class": "date_commit_field"}))
    
    def __init__(self, user, action, *args, **kwargs):
        super(ActionForm, self).__init__(*args, **kwargs)
        self.user = user
        self.action = action
    
    def clean(self):
        if "complete" in self.data:
            self.operation = "complete"
        elif "commitment" in self.data:
            self.operation = "commitment"
        elif "cancel" in self.data:
            self.operation = "cancel"
        else:
            raise forms.ValidationError("No operation was provided.")
        return self.cleaned_data
    
    def save(self):
        uap, created = UserActionProgress.objects.get_or_create(user=self.user,
            action=self.action)
        if self.operation == "complete":
            uap.is_completed = True
            uap.save()
            Record.objects.create_record(request.user, "action_complete", 
                self.action)
        elif self.operation == "commitment":
            uap.date_committed = self.cleaned_data["date_committed"]
            uap.save()
            Record.objects.create_record(self.user, "action_commitment", 
                self.action, data={"date_committed": uap.date_committed})
        elif self.operation == "cancel":
            uap.date_committed = None
            uap.save()