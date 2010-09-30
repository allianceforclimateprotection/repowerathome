# coding: utf-8

from django import forms
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from actions.models import Action
from messaging.models import Stream

from models import Survey, Commitment, ContributorSurvey

class ActionChoiceField(forms.ChoiceField):
    def __init__(self, action, *args, **kwargs):
        super(ActionChoiceField, self).__init__(*args, **kwargs)
        self.action = action
        
class SurveyForm(forms.ModelForm):
    CHOICES = (
        ("D", ""),
        ("C", ""),
    )
    action_slugs = ()
    
    class Meta:
        model = Survey
        exclude = ("name", "event_type", "form_name", "template_name", "is_active", "contributors",)
        
    def __init__(self, contributor, entered_by, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.contributor = contributor
        self.entered_by = entered_by
        self.instance = Survey.objects.get(form_name=self.__class__.__name__)
        data = {}
        for commitment in Commitment.objects.filter(contributor=contributor):
            field = self.fields.get(commitment.question, None)
            if field:
                field.initial = field.to_python(commitment.answer)
        for slug in self.action_slugs:
            action = Action.objects.get(slug=slug)
            self.fields[action.slug.replace('-', '_')] = ActionChoiceField(action=action,
                choices=SurveyForm.CHOICES, widget=forms.CheckboxSelectMultiple,
                required=False, label=action.name)
    
    def save(self, *args, **kwargs):
        for field, data in self.cleaned_data.items():
            commitment, created = Commitment.objects.get_or_create(contributor=self.contributor, 
                question=field)
            commitment.answer = data
            if hasattr(self.fields[field], "action"):
                commitment.action = self.fields[field].action
                if commitment.answer == "C":
                    if created:
                        Stream.objects.get(slug="commitment").enqueue(content_object=commitment, 
                            start=commitment.created, end=commitment.date_committed,
                            batch_content_object=self.contributor)
                    else:
                        Stream.objects.get(slug="commitment").upqueue(content_object=commitment, 
                            start=commitment.updated, end=commitment.date_committed,
                            batch_content_object=self.contributor)
                else:
                    Stream.objects.get(slug="commitment").dequeue(content_object=commitment)
            commitment.save()
        ContributorSurvey.objects.get_or_create(contributor=self.contributor, survey=self.instance,
            entered_by=self.entered_by)

class EnergyMeetingCommitmentCard(SurveyForm):
    host_event = forms.BooleanField(required=False, label="Host an event")
    join_team = forms.BooleanField(required=False, label="Join a team")
    action_slugs = ("eliminate-standby-vampire-power", "programmable-thermostat",
        "change-air-conditioning-heater-filters", "have-home-energy-audit")
    
class EnergyMeetingCommitmentCardVersion2(EnergyMeetingCommitmentCard):
    organize = forms.BooleanField(required=False, label="Organize my community to save energy")
    
class ApartmentEnergyMeetingCommitmentCard(EnergyMeetingCommitmentCard):
    action_slugs = ("eliminate-standby-vampire-power", "programmable-thermostat",
        "replace-your-incandescent-light-bulbs-with-cfls", "wash-clothes-cold-water")
    
class ApartmentEnergyMeetingCommitmentCardVersion2(ApartmentEnergyMeetingCommitmentCard):
    organize = forms.BooleanField(required=False, label="Organize my community to save energy")

class PilotEnergyMeetingCommitmentCard(SurveyForm):
    action_slugs = (a.slug for a in Action.objects.all())

    
class VolunteerInterestForm(SurveyForm):
    action_slugs = ("eliminate-standby-vampire-power", "programmable-thermostat")
    school = forms.BooleanField(required=False)
    workplace = forms.BooleanField(required=False)
    club = forms.BooleanField(required=False)
    neighborhood = forms.BooleanField(required=False)
    faith = forms.BooleanField(required=False)
    