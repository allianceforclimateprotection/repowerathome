import os
import re

def local_join(path):
    """Convenience function for path joining"""
    return os.path.join(os.path.dirname(__file__), path)

def hash_val(value):
    """Creates a SHA1 hash of a value with the secret key"""
    import hashlib
    from django.conf import settings
    if not value: 
        raise Exception("Cannot hash a value that evaluates to False")
    try:
        hash_string = ""
        for item in value:
            hash_string += unicode(item)
    except:
        hash_string = unicode(value)

    return hashlib.sha1("%s%s" % (settings.SECRET_KEY, hash_string)).hexdigest()

QUOTE_REGEX = re.compile("""^('.*')|(".*")$""")
def strip_quotes(val):
    """Remove quote from a value"""
    return val[1:-1] if QUOTE_REGEX.match(val) else val
    
def forbidden(request, message="You do not have permissions."):
    """Return a 500 page with a given message"""
    from django.http import HttpResponseForbidden
    from django.template import loader, RequestContext
    return HttpResponseForbidden(loader.render_to_string('403.html', { 'message':message, }, RequestContext(request)))
    
def hex_to_byte(hex_str):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    byte_list = []
    hex_str = ''.join(hex_str.split(" "))
    for i in range(0, len(hex_str), 2):
        byte_list.append(chr(int(hex_str[i:i+2], 16)))
    return ''.join(byte_list)