from __future__ import with_statement
import re
import urllib2

from fabric.api import *
from fabric.contrib.console import confirm

env.user = "ubuntu"
env.key_filename = "/Users/buckley/.ssh/acp-ec2-pk.pem"

env.roledefs = {
    "web": ["prod1.repowerathome.com", "prod2.repowerathome.com"],
    "loadbalancer": ["loadbalancer.repowerathome.com"],
    "media": ["rahstatic.s3.amazonaws.com"],
    "database": ["database.repowerathome.com"],
    "development": ["dev.repowerathome.com"],
    "staging": ["staging.repowerathome.com"],
}

env.deploy_to = "$HOME/webapp"
env.parent = "origin"
env.branch = "master"
env.revision = "HEAD"
env.repository = "git@codebasehq-deploy:rah/rah/rah.git"

def dev():
    env.hosts = env.roledefs["development"]
def staging():
    env.hosts = env.roledefs["staging"]
def prod():
    env.hosts = env.roledefs["web"]
def dummy():
    env.hosts = ["ec2-184-73-53-153.compute-1.amazonaws.com"]
deployments = [dev, staging, prod, dummy]


def test():
    "Run all tests"
    with settings(warn_only=True):
        result = local("./hooks/pre-commit", capture=False)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def clean():
    "Remove all the .pyc files from the deploy directory"
    if env.hosts:
        run("cd %(deploy_to)s && find . -name '*.pyc' -depth -exec rm {} \;" % env)
    else:
        local("find . -name '*.pyc' -depth -exec rm {} \;")
        
def enable_maintenance_page():
    "Turns on the maintenance page"
    require("deploy_to", provided_by=deployments)
    run("cd %(deploy_to)s/static && cp maintenance.html.disabled maintenance.html" % env)
    
def install_requirements():
    "Using pip install all of the requirements defined"
    require("deploy_to", provided_by=deployments)
    sudo("cd %(deploy_to)s/../requirements && pip install -r %(deploy_to)s/requirements.txt" % env)
    
def reset():
    "Set the workspace to the desired revision"
    require("deploy_to", provided_by=deployments)
    with cd("%(deploy_to)s" % env):
        run("git checkout master && git reset --hard HEAD")
    
def pull():
    "Updates the application with new code"
    require("deploy_to", provided_by=deployments)
    run("cd %(deploy_to)s && git pull --ff-only %(parent)s %(branch)s" % env)
    
def checkout():
    "Checkout the revision you would like to deploy"
    require("deploy_to", provided_by=deployments)
    run("cd %(deploy_to)s && git checkout %(revision)s" % env)
    
@runs_once
def minify():
    "Minify the js and css files"
    require("deploy_to", provided_by=deployments)
    run("cd %(deploy_to)s/static/minify && ./minify.sh" % env)
    
@runs_once
def s3sync():
    "Sync static data with our s3 bucket"
    require("deploy_to", provided_by=deployments)
    run("cd %(deploy_to)s && python manage.py sync_media_s3 --gzip --force" % env)
    
@runs_once
def backupdb():
    "Create a backup of the database"
    pass

@runs_once
def migratedb():
    "Migrate the database"
    require("deploy_to", provided_by=deployments)
    if confirm("Would you like to migrate the database?"):
        run("cd %(deploy_to)s && python manage.py migrate" % env)
    
@runs_once
def syncdb():
    "Sync the database with any new models"
    require("deploy_to", provided_by=deployments)
    run("cd %(deploy_to)s && python manage.py syncdb" % env) # can this handle stdin over ssh
    
def restart_apache():
    "Reboot Apache2 server."
    sudo("/etc/init.d/apache2 restart")
    
def disable_maintenance_page():
    "Turns off the maintenance page"
    require("deploy_to", provided_by=deployments)
    run("cd %(deploy_to)s/static && rm maintenance.html" % env)
    
@runs_once
def notify_codebase():
    "Notify codebase that a new revision has been deployed"
    match = re.search("git\@(codebasehq-deploy):(.*)\/(.*)\/(.*)\.git", env.repository)
    domain = "%s.codebasehq.com" % match.group(2)
    project = match.group(3)
    repository = match.group(4)
    username = local("git config codebase.username").strip()
    api_key = local("git config codebase.apikey").strip()
    
    xml = []
    xml.append("<deployment>")
    xml.append("<servers>%s</servers>" % ",".join(env.hosts))
    xml.append("<revision>%(revision)s</revision>" % env)
    xml.append("<environment>%(deploy_to)s</environment>" % env)
    xml.append("<branch>%(branch)s</branch>" % env)
    xml.append("</deployment>")
    
    headers = {"Content-Type": "application/xml", "Accept": "application/xml"}
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password(realm="Codebase",
                              uri="http://%s/" % domain,
                              user=username,
                              passwd=api_key)
    opener = urllib2.build_opener(auth_handler)
    # ...and install it globally so it can be used with urlopen.
    urllib2.install_opener(opener)
    request = urllib2.Request("http://%s/%s/%s/deployments" % (domain, project, repository), 
        "".join(xml), headers)

def deploy(revision=None, sync_media=True):
    "Deploy code to server"
    if revision: env.revision = revision
    require("deploy_to", provided_by=deployments)
    # enable_maintenance_page()
    install_requirements()
    reset()
    pull()
    checkout()
    minify()
    if bool(sync_media) and sync_media.upper() != "FALSE":
        s3sync()
    #backupdb()
    migratedb()
    syncdb()
    restart_apache()
    # disable_maintenance_page()
    notify_codebase()
    print("\e[32m(branch)s:%(revision)s has been deployed to %(hosts)s\e[0m" % env)