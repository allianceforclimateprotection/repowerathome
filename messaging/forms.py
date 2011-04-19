from django import forms
from django.contrib import auth
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.forms.widgets import CheckboxSelectMultiple
from django.template import Context, loader

from models import Stream, StreamBlacklist

class StreamNotificationsForm(forms.Form):
    stream_notifications = forms.ModelMultipleChoiceField(required=False, queryset=None,
        widget=forms.CheckboxSelectMultiple, help_text="By selecting a reminder type, you have elected to \
        recieve reminder emails pertaining to that activity.", label="Reminder email notifications")

    def __init__(self, user, *args, **kwargs):
        super(StreamNotificationsForm, self).__init__(*args, **kwargs)
        self.user = user
        self.streams = Stream.objects.filter(can_unsubscribe=True)
        self.fields["stream_notifications"].queryset = self.streams
        self.not_blacklisted = [s.pk for s in Stream.objects.streams_not_blacklisted_by_user(user)]
        self.fields["stream_notifications"].initial = self.not_blacklisted

    def save(self):
        notifications = self.cleaned_data["stream_notifications"]
        for stream in self.streams:
            if not stream in notifications and stream.pk in self.not_blacklisted:
                StreamBlacklist.objects.create(user=self.user, stream=stream)
            if stream in notifications and stream.pk not in self.not_blacklisted:
                StreamBlacklist.objects.get(user=self.user, stream=stream).delete()
