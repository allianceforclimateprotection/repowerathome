from datetime import date, datetime
import os
import random
import re
import time

def local_join(x):
    return os.path.join(os.path.dirname(__file__), x)

def hash_val(value):
    import hashlib
    from django.conf import settings
    if not value: raise Exception("Cannot hash a value that evaluates to False")
    try:
        hash_string = ""
        for item in value:
            hash_string += unicode(item)
    except:
        hash_string = unicode(value)

    return hashlib.sha1("%s%s" % (settings.SECRET_KEY, hash_string)).hexdigest()

QUOTE_REGEX = re.compile("""^('.*')|(".*")$""")
def strip_quotes(val):
    return val[1:-1] if QUOTE_REGEX.match(val) else val
    
def forbidden(request, message="You do not have permissions."):
    from django.http import HttpResponseForbidden
    from django.template import Context, loader, RequestContext
    return HttpResponseForbidden(loader.render_to_string('403.html', { 'message':message, }, RequestContext(request)))
    
def hex_to_byte(hex_str):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    bytes = []
    hex_str = ''.join(hex_str.split(" "))
    for i in range(0, len(hex_str), 2):
        bytes.append(chr(int(hex_str[i:i+2], 16)))
    return ''.join(bytes)
    
def make_token():
    from django.utils.http import int_to_base36
    datestamp = (date.today() - date(2001,1,1)).days
    # timestamp is number of days since 2001-1-1.  Converted to
    # base 36, this gives us a 3 digit string until about 2121
    ds_b36 = int_to_base36(datestamp)
    
    now = datetime.now()
    timestamp = (3600000000*now.hour + 60000000*now.minute + 1000000*now.second + now.microsecond)
    ts_b36 = int_to_base36(timestamp)

    # We limit the hash to 20 chars to keep URL short
    from django.conf import settings
    from django.utils.hashcompat import sha_constructor
    hash = sha_constructor(settings.SECRET_KEY + unicode(random.random()) + 
                           unicode(datestamp)).hexdigest()[::2]
    return "%s%s%s" % (ds_b36, ts_b36, hash)