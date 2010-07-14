from django import forms
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from actions.models import Action

from models import Survey, Commitment
from widgets import RadioRendererForTable

class ActionChoiceField(forms.ChoiceField):
    def __init__(self, action_slug, *args, **kwargs):
        super(ActionChoiceField, self).__init__(*args, **kwargs)
        self.action = Action.objects.get(slug=action_slug)
        
class ActionBooleanField(forms.BooleanField):
    def __init__(self, action_slug, *args, **kwargs):
        super(ActionBooleanField, self).__init__(*args, **kwargs)
        self.action = Action.objects.get(slug=action_slug)
        
    def get_prep_value(self, value):
        return value == "C"
        
    def to_python(self, value):
        return "C" if value else ""
        
class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        exclude = ("name", "event_type", "form_name", "template_name", "is_active",)
        
    def __init__(self, guest, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.guest = guest
        data = {}
        for commitment in Commitment.objects.filter(guest=guest, survey=self.instance):
            field = self.fields[commitment.question]
            field.initial = field.to_python(commitment.answer)
    
    def save(self, *args, **kwargs):
        for field, data in self.cleaned_data.items():
            commitment, created = Commitment.objects.get_or_create(guest=self.guest, 
                survey=self.instance, question=field)
            commitment.answer = data
            if hasattr(self.fields[field], "action"):
                commitment.action = self.fields[field].action
            commitment.save()

class EnergyMeetingCommitmentCard(SurveyForm):
    CHOICES = (
        ("D", "I've Done this"),
        ("C", "I pledge to do this"),
    )
    eliminate_vampire = ActionChoiceField(action_slug="eliminate-standby-vampire-power",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Eliminate vampire power")
    program_thermostat = ActionChoiceField(action_slug="programmable-thermostat",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Program your thermostat")
    replace_filter = ActionChoiceField(action_slug="change-air-conditioning-heater-filters",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Replace your HVAC filter")
    energy_audit = ActionChoiceField(action_slug="have-home-energy-audit",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Have an energy audit")
    host_event = forms.BooleanField(required=False, label="Host an event")
    join_team = forms.BooleanField(required=False, label="Join a team")
    
class VolunteerInterestForm(SurveyForm):

    eliminate_vampire = ActionBooleanField(action_slug="eliminate-standby-vampire-power",
        required=False)
    program_thermostat = ActionBooleanField(action_slug="programmable-thermostat",
        required=False)
    
    school = forms.BooleanField(required=False)
    workplace = forms.BooleanField(required=False)
    club = forms.BooleanField(required=False)
    neighborhood = forms.BooleanField(required=False)
    faith = forms.BooleanField(required=False)
    