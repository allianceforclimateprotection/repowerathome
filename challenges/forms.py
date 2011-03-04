from django import forms

from commitments.models import Contributor
from commitments.forms import ContributorForm

from models import Challenge, Support

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ('title', 'description', 'goal',)

class PetitionForm(ContributorForm):
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
