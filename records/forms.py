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
            link = "http://%s%s" % (Site.objects.get_current().domain, last_record.get_absolute_url())
            publish_message(request.user, message, link)
        if network == "t":
            profile = request.user.get_profile()
            profile.twitter_share = True
            profile.save()
        return True
            