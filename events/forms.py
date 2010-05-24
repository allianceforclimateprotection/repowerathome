from django import forms

from geo.models import Location

from models import Event

STATES = ("AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "IA", "ID", 
    "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", 
    "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", 
    "UT", "VA", "VT", "WA", "WI", "WV", "WY",)
    
def _times():
    times = []
    for meridiem in ["am", "pm"]:
        for hour in [12] + range(1,12):
            for minute in [0,15,30,45]:
                times.append("%0.2d:%0.2d%s" % (hour, minute, meridiem))
    return times
TIMES = _times()

class EventForm(forms.ModelForm):
    city = forms.CharField(required=False, max_length=50)
    state = forms.ChoiceField(required=False, choices=[(state, state) for state in STATES])
    zipcode = forms.CharField(required=False, max_length=5)
    is_private = forms.ChoiceField(choices=((True, "Yes"), (False, "No")), initial=False,
        widget=forms.RadioSelect)
    
    class Meta:
        model = Event
        fields = ["event_type", "where", "city", "state", "zipcode", "when", "start", "end", 
            "details", "is_private"]
        widgets = {
            "event_type": forms.RadioSelect(choices=Event.EVENT_TYPES),
            "when": forms.TextInput(attrs={"class": "datepicker"}),
            "start": forms.Select(choices=[(time, time) for time in TIMES]),
            "end": forms.Select(choices=[(time, time) for time in TIMES]),
        }
        
    def clean_zipcode(self):
        data = self.cleaned_data["zipcode"]
        if data:
            try:
                self.cleaned_data["location"] = Location.objects.get(zipcode=data)
            except Location.DoesNotExist:
                raise forms.ValidationError("Invalid zipcode %s" % data)
        return data
        
    def clean(self):
        if not "location" in self.cleaned_data:
            city = self.cleaned_data.get("city", None)
            state = self.cleaned_data.get("state", None)
            if city and state:
                locations = Location.objects.filter(name__iexact=city, st=state)
                if not locations:
                    raise forms.ValidationError("Invalid place %s, %s" % (city, state))
                self.cleaned_data["location"] = locations[0]
            else:
                raise forms.ValidationError("You must specify city and state or a zipcode")
        return self.cleaned_data
        
    def save(self, *args, **kwargs):
        self.instance.location = self.cleaned_data["location"]
        return super(EventForm, self).save(*args, **kwargs)
        
                