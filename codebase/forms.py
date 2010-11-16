from django import forms

from models import Ticket

class TestingFeedbackForm(forms.Form):
    ticket_id = forms.IntegerField(widget=forms.HiddenInput)
    works = forms.ChoiceField(choices=(("yes", "yes"), ("no", "no")), widget=forms.RadioSelect, label="Did it work?")
    name = forms.CharField(label="What's your name?")
    feedback = forms.CharField(label="Any feedback?", widget=forms.Textarea(attrs={"cols": "25", "rows": "4"}))
    
    def save(self, request):
        ticket_id = self.cleaned_data["ticket_id"]
        self.cleaned_data["useragent"] = request.META['HTTP_USER_AGENT']
        message = """
**Name**:   %(name)s  
**Works**:      %(works)s  
**Feedback**:   %(feedback)s  
**User Agent**: %(useragent)s  
""" % self.cleaned_data
        return Ticket.objects.add_feedback(ticket_id, message)
    