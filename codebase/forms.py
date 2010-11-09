from django import forms

from models import Ticket

class TestingFeedbackForm(forms.Form):
    # ticket = forms.ChoiceField(choices=[(t.ticket_id, t.summary) for t in Ticket.objects.qa_tickets()])
    ticket_id = forms.IntegerField(widget=forms.HiddenInput)
    works = forms.ChoiceField(choices=(("yes", "yes"), ("no", "no")), widget=forms.RadioSelect, label="Did it work?")
    initials = forms.CharField(label="What's your name?")
    feedback = forms.CharField(label="Any feedback?", widget=forms.Textarea(attrs={"cols": "25", "rows": "4"}))
    
    def save(self):
        ticket_id = self.cleaned_data["ticket_id"]
        message = """
**Initials**:   %(initials)s  
**Works**:      %(works)s  
**Feedback**:   %(feedback)s  
""" % self.cleaned_data
        Ticket.objects.add_feedback(ticket_id, message)
    