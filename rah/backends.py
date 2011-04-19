from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.validators import email_re

class EmailBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, username=None, password=None, is_facebook_connect=False):
        #If username is an email address, then try to pull it up
        if email_re.search(username):
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            #We have a non-email address username we should try username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        if is_facebook_connect or \
            (user.check_password(password) and not user.get_profile().facebook_connect_only):
            # Either the user is loging in via facebook, or they are loging in with a password
            # if the later make sure the user has not been created to allow only facebook logins
            return user
