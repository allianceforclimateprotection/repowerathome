import os
import sys

def local_join(x):
    return os.path.join(os.path.dirname(__file__), x)