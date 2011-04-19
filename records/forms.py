from django import forms
from django.contrib.sites.models import Site

from facebook_app.models import publish_message

from models import Record

class AskToShareForm(forms.Form):
    SOCIAL_NETWORKS = (
        # ("t", "Twitter",),
        ("f", "Facebook",),
    )
    social_network = forms.ChoiceField(label="", choices=SOCIAL_NETWORKS, widget=forms.RadioSelect)
    has_twitter_access = forms.BooleanField(widget=forms.HiddenInput, required=False)
    has_facebook_access = forms.BooleanField(widget=forms.HiddenInput, required=False)

    def __init__(self, request, *args, **kwargs):
        super(AskToShareForm, self).__init__(*args, **kwargs)
        profile = request.user.get_profile()
        self.fields["has_twitter_access"].initial = bool(profile.twitter_access_token)
        self.fields["has_facebook_access"].initial = bool(profile.facebook_access_token)

    def save(self, request, *args, **kwargs):
        network = self.cleaned_data["social_network"]
        profile = request.user.get_profile()
        if network == "f":
            if not profile.facebook_access_token:
                return False
            profile.facebook_share = True
            profile.save()
            # now post their last record
            last_record = Record.objects.user_records(user=request.user, quantity=1)[0]
            message = last_record.render_for_social(request)
            message = message.encode("utf-8")
            link = "http://%s%s?source=sm-fb-post&subsource=%s" % (Site.objects.get_current().domain,
                last_record.get_absolute_url(), last_record.get_absolute_url())
            publish_message(request.user, message, link)
        if network == "t":
            profile = request.user.get_profile()
            profile.twitter_share = True
            profile.save()
        return True

