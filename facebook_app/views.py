import facebook
import hashlib

from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.admin.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import loader, Context

from rah.models import Profile
from rah.signals import logged_in

def login(request):
    facebook_user = facebook.get_user_from_cookie(request.COOKIES, 
        settings.FACEBOOK_APPID, settings.FACEBOOK_SECRET)
    next = request.GET.get("next", None)
    if facebook_user:
        access_token = facebook_user["access_token"]
        graph = facebook.GraphAPI(access_token)
        facebook_user = graph.get_object("me")
        email = facebook_user["email"]
        if graph:
            try:
                profile = Profile.objects.get(facebook_access_token=access_token)
            except Profile.DoesNotExist:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    username = hashlib.md5(email).hexdigest()[:30] 
                    user = User.objects.create_user(username, email, "")
                    user.first_name = facebook_user["first_name"]
                    user.last_name = facebook_user["last_name"]
                    user.save()
                profile = user.get_profile()
                profile.facebook_access_token = access_token
                profile.facebook_connect_only = "username" in locals()
                profile.save()
            user = auth.authenticate(username=profile.user.email, is_facebook_connect=True)
            logged_in.send(sender=None, request=request, user=user, is_new_user="username" in locals())
            auth.login(request, user)
            return redirect(next or "index")
    messages.error("Facebook login credentials could not be verified, please try again.")
    return redirect(next or "login")    