import os
import sys

def local_join(x):
    return os.path.join(os.path.dirname(__file__), x)

def hash_val(value):
    import hashlib
    from settings import SECRET_KEY
    return hashlib.sha1("%s%s" % (SECRET_KEY, value)).hexdigest()