import base64
import re
import urllib2

from fabric.api import env, local, runs_once

def _send_codebase(path, data=None):
    "POST the given data message to the codebase API, if no data is provided GET"
    match = re.search("git\@codebasehq\.com:(.*)\/(.*)\/.*\.git", env.repository)
    domain = "%s.codebasehq.com" % match.group(1)
    project = match.group(2)
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
    require("deploy_to", provided_by=DEPLOY_SERVERS)
    repository = re.search("git\@codebasehq\.com:.*\/.*\/(.*)\.git", env.repository).group(1)

    xml = []
    xml.append("<deployment>")
    xml.append("<servers>%s</servers>" % ",".join(env.hosts))
    xml.append("<revision>%(sha)s</revision>" % env)
    xml.append("<environment>%(environment)s</environment>" % env)
    xml.append("<branch>%(revision)s</branch>" % env)
    xml.append("</deployment>")

    _send_codebase("/%s/deployments" % repository, "".join(xml))