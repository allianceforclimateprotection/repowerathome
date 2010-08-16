import os

from django import template
from django.conf import settings

from utils import strip_quotes

register = template.Library()

class DatedStaticNode(template.Node):
    def __init__(self, static_file):
        self.static_file = static_file
    
    def render(self, context):
        # figure out if we need to use https media url
        meta = context.get("request").META
        if 'HTTP_X_URL_SCHEME' in meta and meta['HTTP_X_URL_SCHEME'] == 'https' and settings.get("MEDIA_URL_HTTPS"):
            media_url = settings.MEDIA_URL_HTTPS
        else:
            media_url = settings.MEDIA_URL
            
        try:
            abs_path = os.path.join(settings.MEDIA_ROOT, self.static_file)
            paths = os.path.split(self.static_file)
            m_time = int(os.stat(abs_path).st_mtime)
            return os.path.join(media_url, os.path.join(paths[0], "%s?%s" % (paths[1], m_time)))
        except:
            return os.path.join(media_url, self.static_file)
        

@register.tag
def dated_static(parser, token):
    bits = token.contents.split()
    if len(bits) <> 2:
        raise template.TemplateSyntaxError("Wrong number of arguments passed. All we need is the path")
    
    return DatedStaticNode(strip_quotes(bits[1]))
