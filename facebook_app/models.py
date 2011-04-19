import facebook

from django.db import models

def _get_graph(user):
    profile = user.get_profile()
    if profile.facebook_access_token:
        graph = facebook.GraphAPI(profile.facebook_access_token)
        try:
            graph.get_object("me") # test the graph to see if the token works
            return graph
        except facebook.GraphAPIError:
            # token is invalid, delete it
            profile.facebook_access_token = None
            profile.facebook_share = False
            profile.save()
    return None

def facebook_profile(user, size="small"):
    graph = _get_graph(user)
    if not graph:
        return None
    facebook_user = graph.get_object("me")
    return "http://graph.facebook.com/%s/picture?type=%s" % (facebook_user["id"], size)
    
def publish_message(user, message, link):
    graph = _get_graph(user)
    if not graph:
        return None
    return graph.put_wall_post(message=message, attachment={"link": link})