# coding: utf-8

from django import forms

from actions.models import Action
from messaging.models import Stream
from geo.models import Location

from models import Survey, Commitment, Contributor, ContributorSurvey

class ActionChoiceField(forms.ChoiceField):
    CHOICES = (
        ("C", ""),
        ("D", ""),
    )
    
    def __init__(self, action, *args, **kwargs):
        super(ActionChoiceField, self).__init__(*args, **kwargs)
        self.action = action

    def to_python(self, value):
        if value and isinstance(value, (list, tuple)):
            return value[0]
        return value
        
class SurveyForm(forms.ModelForm):
    action_slugs = ()
    
    class Meta:
        model = Survey
        exclude = ("name", "event_type", "form_name", "template_name", "is_active", "contributors", "label",)
        
    def __init__(self, contributor, entered_by, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.contributor = contributor
        self.entered_by = entered_by
        self.instance = Survey.objects.get(form_name=self.__class__.__name__)
        for slug in self.action_slugs:
            action = Action.objects.get(slug=slug)
            self.fields[action.slug.replace('-', '_')] = ActionChoiceField(action=action,
                choices=ActionChoiceField.CHOICES, widget=forms.CheckboxSelectMultiple,
                required=False, label=action.name)
        for commitment in Commitment.objects.filter(contributor=contributor):
            field = self.fields.get(commitment.question, None)
            if field:
                field.initial = field.to_python(commitment.answer)

    
    def save(self, *args, **kwargs):
        for field, data in self.cleaned_data.items():
            commitment, created = Commitment.objects.get_or_create(contributor=self.contributor, question=field)
            commitment.answer = data if not data == [] else ""
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

class VampireHuntCommitmentCard(SurveyForm):
    volunteer = forms.BooleanField(required=False, label="I want to volunteer with Repower at Home")
    action_slugs = ("eliminate-standby-vampire-power",)
    
class VolunteerInterestForm(SurveyForm):
    action_slugs = ("eliminate-standby-vampire-power", "programmable-thermostat")
    school = forms.BooleanField(required=False)
    workplace = forms.BooleanField(required=False)
    club = forms.BooleanField(required=False)
    neighborhood = forms.BooleanField(required=False)
    faith = forms.BooleanField(required=False)
    
class PledgeCard(SurveyForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    zipcode = forms.CharField(max_length=10, required=False, help_text="Leave blank if not a US resident")
    pledge = forms.BooleanField(required=False, widget=forms.HiddenInput)
    
    def __init__(self, contributor, *args, **kwargs):
        super(PledgeCard, self).__init__(contributor, None, *args, **kwargs)
        self.location = None        
        if contributor:
            self.fields["first_name"].initial = contributor.user.first_name
            self.fields["last_name"].initial = contributor.user.last_name
            self.fields["email"].initial = contributor.user.email
    
    def clean_zipcode(self):
        data = self.cleaned_data['zipcode'].strip()
        if data:
            if len(data) <> 5:
                raise forms.ValidationError("Please enter a 5 digit zipcode")
            try:
                self.location = Location.objects.get(zipcode=data)
            except Location.DoesNotExist, e:
                raise forms.ValidationError("Zipcode is invalid")
        return data
        
    def save(self, *args, **kwargs):
        try:
            contributor = Contributor.objects.get(email=self.cleaned_data["email"])
        except Contributor.DoesNotExist:
            contributor = Contributor.objects.create(first_name=self.cleaned_data["first_name"], 
                last_name=self.cleaned_data["last_name"], email=self.cleaned_data["email"],
                location=self.location) 
        commitment, created = Commitment.objects.get_or_create(contributor=contributor, question="pledge")
        commitment.answer = True
        commitment.save()