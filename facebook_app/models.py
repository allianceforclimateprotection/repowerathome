import facebook

from django.db import models

def facebook_profile(user, size="small"):
    profile = user.get_profile()
    if not profile.facebook_access_token:
        return None
    graph = facebook.GraphAPI(profile.facebook_access_token)
    facebook_user = graph.get_object("me")
    return "http://graph.facebook.com/%s/picture?type=%s" % (facebook_user["id"], size)
