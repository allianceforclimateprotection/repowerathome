from django import forms

from models import Event

STATES = ("AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "IA", "ID", 
    "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", 
    "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", 
    "UT", "VA", "VT", "WA", "WI", "WV", "WY",)

class EventForm(forms.ModelForm):
    city = forms.CharField(max_length=50)
    state = forms.ChoiceField(choices=[(state, state) for state in STATES])
    zipcode = forms.CharField(max_length=5)
    
    class Meta:
        model = Event
        fields = ["event_type", "where", "city", "state", "zipcode", "when", "start", "end", 
            "details", "is_private"]
        widgets = {
            "event_type": forms.RadioSelect(choices=Event.EVENT_TYPES),
            "is_private": forms.RadioSelect(choices=(("Y", "Yes"), ("N", "No")))
        }