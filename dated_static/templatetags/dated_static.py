import os

from django import template
from django.conf import settings

from utils import strip_quotes

register = template.Library()

def timestamp_file(static_file, https=False):
    if https:
        media_url = settings.MEDIA_URL_HTTPS
    else:
        media_url = settings.MEDIA_URL

    try:
        abs_path = os.path.join(settings.MEDIA_ROOT, static_file)
        paths = os.path.split(static_file)
        m_time = int(os.stat(abs_path).st_mtime)
        return os.path.join(media_url, os.path.join(paths[0], "%s?%s" % (paths[1], m_time)))
    except:
        return os.path.join(media_url, static_file)

class DatedStaticNode(template.Node):
    def __init__(self, static_file):
        self.static_file = static_file

    def render(self, context):
        # figure out if we need to use https media url
        meta = context.get("request").META
        if 'SERVER_PORT' in meta and meta['SERVER_PORT'] == '443' and settings.MEDIA_URL_HTTPS:
            https = True
        else:
            https = False

        return timestamp_file(self.static_file, https)


@register.tag
def dated_static(parser, token):
    bits = token.contents.split()
    if len(bits) <> 2:
        raise template.TemplateSyntaxError("Wrong number of arguments passed. All we need is the path")

    return DatedStaticNode(strip_quotes(bits[1]))
