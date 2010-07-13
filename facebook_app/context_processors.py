from django.conf import settings

def facebook_appid(context):
    return {'FACEBOOK_APPID': settings.FACEBOOK_APPID}