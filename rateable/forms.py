from django import forms

from models import Rating
from widgets import IsHelpfulWidget, ThumbsRadio

class RatingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        form = super(RatingForm, self).__init__(*args, **kwargs)
        self.id = "%s_%s" % (self.instance.content_type.pk, self.instance.object_pk)
        self.initial_score = self.initial.get("score", self.fields["score"].initial)
        return form
    
    class Meta:
        model = Rating
        fields = ("content_type", "object_pk", "score")
        widgets = {
            "content_type": forms.HiddenInput,
            "object_pk": forms.HiddenInput,
            "score": ThumbsRadio,
        }