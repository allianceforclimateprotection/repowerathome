# coding: utf-8

from django import forms
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from actions.models import Action
from messaging.models import Stream

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
                if commitment.answer == "C":
                    if created:
                        Stream.objects.get(slug="commitment").enqueue(content_object=commitment, 
                            start=commitment.created, end=commitment.date_committed,
                            batch_content_object=self.guest)
                    else:
                        Stream.objects.get(slug="commitment").upqueue(content_object=commitment, 
                            start=commitment.updated, end=commitment.date_committed,
                            batch_content_object=self.guest)
                else:
                    Stream.objects.get(slug="commitment").dequeue(content_object=commitment)
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
    
class EnergyMeetingCommitmentCardVersion2(EnergyMeetingCommitmentCard):
    organize = forms.BooleanField(required=False, label="Organize my community to save energy")
    
    def __init__(self, *args, **kwargs):
        super(EnergyMeetingCommitmentCardVersion2, self).__init__(*args, **kwargs)
        del self.fields["host_event"]
        del self.fields["join_team"]
    
class ApartmentEnergyMeetingCommitmentCard(EnergyMeetingCommitmentCard):
    replace_light_bulbs = ActionChoiceField(action_slug="replace-your-incandescent-light-bulbs-with-cfls",
        choices=EnergyMeetingCommitmentCard.CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Replace light bulbs with CFLs")
    cold_wash = ActionChoiceField(action_slug="wash-clothes-cold-water",
        choices=EnergyMeetingCommitmentCard.CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Use the cold wash cycle")
        
    def __init__(self, *args, **kwargs):
        super(ApartmentEnergyMeetingCommitmentCard, self).__init__(*args, **kwargs)
        del self.fields["replace_filter"]
        del self.fields["energy_audit"]
    
class ApartmentEnergyMeetingCommitmentCardVersion2(ApartmentEnergyMeetingCommitmentCard):
    organize = forms.BooleanField(required=False, label="Organize my community to save energy")
    
    def __init__(self, *args, **kwargs):
        super(ApartmentEnergyMeetingCommitmentCardVersion2, self).__init__(*args, **kwargs)
        del self.fields["host_event"]
        del self.fields["join_team"]

class PilotEnergyMeetingCommitmentCard(SurveyForm):
    CHOICES = (
        ("D", "I've Done this"),
        ("C", "I pledge to do this"),
    )
    replace_hvac_filter = ActionChoiceField(action_slug="change-air-conditioning-heater-filters",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Change your HVAC filter regularly")
    replace_old_fridge = ActionChoiceField(action_slug="replace-your-outdated-refrigerator",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Replace your outdated refrigerator ")
    retire_refrigerat = ActionChoiceField(action_slug="retire-second-refrigerator",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Retire your second refrigerator")
    seal_vents = ActionChoiceField(action_slug="seal-vents-unoccupied-rooms",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Seal off vents in unoccupied rooms")
    use_fan_in_summer = ActionChoiceField(action_slug="use-ceiling-fan-summer",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Use ceiling fans in the summer")
    water_heater_120deg = ActionChoiceField(action_slug="adjust-water-heater-temperature",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Set your water heater to 120°F")
    insulate_windows = ActionChoiceField(action_slug="insulate-your-windows",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Insulate your windows")
    insulate_wtr_pipes = ActionChoiceField(action_slug="insulate-water-pipes",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Insulate your hot water pipes")
    lowflow_shower = ActionChoiceField(action_slug="install-low-flow-shower-head",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Install a low-flow shower head")
    manual_thermostat = ActionChoiceField(action_slug="save-with-manual-thermostat",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Save money with a manual thermostat")
    program_thermostat = ActionChoiceField(action_slug="programmable-thermostat",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Use a programmable thermostat")
    replace_bulb_cfl = ActionChoiceField(action_slug="replace-your-incandescent-light-bulbs-with-cfls",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Replace five light bulbs with CFLs ")
    energy_audit = ActionChoiceField(action_slug="have-home-energy-audit",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Have a home energy audit and retrofit")
    fan_in_winter = ActionChoiceField(action_slug="use-ceiling-fan-winter",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Use ceiling fans in the winter")
    inst_chm_guard = ActionChoiceField(action_slug="install-chimney-draft-guard",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Install a chimney draft guard")
    inst_sink_aerator = ActionChoiceField(action_slug="install-low-flow-sink-aerator",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Install a low-flow sink aerator")
    insulate_water_htr = ActionChoiceField(action_slug="insulate-water-heater",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Insulate your water heater")
    caulk_windows = ActionChoiceField(action_slug="caulk-around-your-windows",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Caulk around your windows")
    close_firedamper = ActionChoiceField(action_slug="keep-fireplace-damper-closed",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Keep the fireplace damper closed")
    cold_wash_cycle = ActionChoiceField(action_slug="wash-clothes-cold-water",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Use the cold wash cycle")
    computer_to_sleep = ActionChoiceField(action_slug="set-your-computer-sleep-automatically",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Set your computer to sleep automatically")
    elim_always_on_light = ActionChoiceField(action_slug="sensors-timers-for-lights",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Eliminate 'always-on' lights")
    dial_dwn_thermostat = ActionChoiceField(action_slug="dial-down-thermostat",
        choices=CHOICES, widget=forms.RadioSelect(renderer=RadioRendererForTable),
        required=False, label="Dial down your thermostat")     
    
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
    