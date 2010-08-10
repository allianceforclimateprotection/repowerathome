import os

from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def dated_static(static_file):
    try:
        abs_path = os.path.join(settings.MEDIA_ROOT, static_file)
        paths = os.path.split(static_file)
        m_time = int(os.stat(abs_path).st_mtime)
        return os.path.join(settings.MEDIA_URL, os.path.join(paths[0], "%s?%s" % (paths[1], m_time)))
    except:
        return static_file