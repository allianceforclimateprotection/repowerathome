from django.conf import settings

def facebook_appid(request):
    return {'FACEBOOK_APPID': settings.FACEBOOK_APPID}