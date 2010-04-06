import os
import re
import sys

def local_join(x):
    return os.path.join(os.path.dirname(__file__), x)

def hash_val(value):
    import hashlib
    from settings import SECRET_KEY
    if not value: raise Exception("Cannot hash a value that evaluates to False")
    try:
        hash_string = ""
        for item in value:
            hash_string += unicode(item)
    except:
        hash_string = unicode(value)

    return hashlib.sha1("%s%s" % (SECRET_KEY, hash_string)).hexdigest()
    
def strip_quotes(val):
    return val[1:-1] if re.match("""^('.*')|(".*")$""", val) else val