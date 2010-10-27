import re

from fabric.api import local

def query_revision(treeish="HEAD"):
    if re.match("^[0-9a-f]{40}$", treeish): return treeish
    return local("git show %s | sed q | cut -d ' ' -f 2" % treeish)