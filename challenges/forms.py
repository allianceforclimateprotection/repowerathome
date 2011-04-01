from django import forms

from commitments.models import Contributor
from commitments.forms import ContributorForm

from models import Challenge, Support

class ChallengeForm(forms.ModelForm):
    goal = forms.IntegerField(min_value=1, help_text="How many petitions do you want to collect?")

    class Meta:
        model = Challenge
        fields = ('title', 'description', 'goal',)

class PetitionForm(ContributorForm):
    first_name = forms.CharField(min_length=2, widget=forms.TextInput(attrs={'class':'form_row_half'}))
    last_name = forms.CharField(min_length=1, widget=forms.TextInput(attrs={'class':'form_row_half form_row_half_last'}))

    class Meta:
        model = Contributor
        fields = ('first_name', 'last_name', 'email',)

    def __init__(self, challenge, *args, **kwargs):
        self.challenge = challenge
        super(PetitionForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        contributor = super(PetitionForm, self).save(*args, **kwargs)
        support, created = Support.objects.get_or_create(challenge=self.challenge,
            contributor=contributor)
        return support
