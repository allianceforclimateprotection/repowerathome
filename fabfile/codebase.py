import base64
import re
import urllib2

from fabric.api import env, local, runs_once, require

def _send_codebase(path, data=None):
    "POST the given data message to the codebase API, if no data is provided GET"
    match = re.search("git\@(codebasehq.*):(.*)\/(.*)\/.*\.git", env.repository)
    domain = "%s.%s" % (match.group(2), match.group(1))
    project = match.group(3)
    username = local("git config codebase.username").strip()
    api_key = local("git config codebase.apikey").strip()
    
    url = "https://%s/%s%s" % (domain, project, path)
    headers = {"Content-type": "application/xml", "Accept": "application/xml", 
        "Authorization": "Basic %s" % base64.b64encode("%s:%s" % (username, api_key))}
    request = urllib2.Request(url, data, headers)
    return urllib2.urlopen(request).read()

@runs_once
def codebase_deployment():
    "Notify codebase that a new revision has been deployed"
    require("sha", "environment", "revision")
    repository = re.search("git\@codebasehq.*:.*\/.*\/(.*)\.git", env.repository).group(1)

    xml = []
    xml.append("<deployment>")
    xml.append("<servers>%s</servers>" % ",".join(env.all_hosts))
    xml.append("<revision>%(sha)s</revision>" % env)
    xml.append("<environment>%(environment)s</environment>" % env)
    xml.append("<branch>%(revision)s</branch>" % env)
    xml.append("</deployment>")

    _send_codebase("/%s/deployments" % repository, "".join(xml))