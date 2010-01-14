import oauth, json

from django import forms
from utils import *

class StatusForm(forms.Form):
    """docstring for AccountForm"""
    status = forms.CharField(max_length=140, widget=forms.Textarea)
        
    def save(self, profile):
        status = self.cleaned_data["status"]
        access_token = profile.twitter_access_token
        token = oauth.OAuthToken.from_string(access_token)
        if token:
            response = json.loads(update_status(token, status))
            # TODO Give some points for this
            if not response.has_key("error"):
                return True
        return False