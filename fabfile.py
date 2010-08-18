from __future__ import with_statement
import base64
import re
import urllib2

from fabric.api import *
from fabric.contrib.console import confirm

env.user = "ubuntu"
env.key_filename = "/Users/buckley/.ssh/acp-ec2-pk.pem"
env.disable_known_hosts = True

env.roledefs = {
    "web": ["prod1.repowerathome.com", "prod2.repowerathome.com"],
    "loadbalancer": ["loadbalancer.repowerathome.com"],
    "development": ["dev.repowerathome.com"],
    "staging": ["staging.repowerathome.com"],
}

env.deploy_to = "/home/%(user)s/webapp" % env
env.parent = "origin"
env.branch = "master"
env.revision = "HEAD"
env.repository = "git@codebasehq-deploy:rah/rah/rah.git"

SHOW_MAINTENANCE_PAGE = False
def dev():
    env.hosts = env.roledefs["development"]
def staging():
    env.hosts = env.roledefs["staging"]
def prod():
    env.hosts = env.roledefs["web"]
    SHOW_MAINTENANCE_PAGE = True
deployments = [dev, staging, prod]

def _determine_environment():
    for key,value in env.roledefs.items():
        if value == env.hosts:
            return key
    return None

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

@roles("loadbalancer")
def enable_maintenance_page():
    "Turns on the maintenance page"
    if SHOW_MAINTENANCE_PAGE:
        sudo("rm /etc/nginx/sites-enabled/rah")
        sudo("ln -s /etc/nginx/sites-available/maintenance /etc/nginx/sites-enabled/maintenance")
        sudo("/etc/init.d/nginx reload")
    
def reset():
    "Set the workspace to the desired revision"
    require("hosts", provided_by=deployments)
    with cd("%(deploy_to)s" % env):
        run("git checkout master && git reset --hard HEAD")
    
def pull():
    "Updates the application with new code"
    require("hosts", provided_by=deployments)
    run("cd %(deploy_to)s && git pull --ff-only %(parent)s %(branch)s" % env)
    
def checkout():
    "Checkout the revision you would like to deploy"
    require("hosts", provided_by=deployments)
    run("cd %(deploy_to)s && git checkout %(revision)s" % env)

def install_requirements():
    "Using pip install all of the requirements defined"
    require("hosts", provided_by=deployments)
    sudo("cd %(deploy_to)s/../requirements && pip install -r %(deploy_to)s/requirements.txt" % env)
    
@runs_once
def minify():
    "Minify the js and css files"
    require("hosts", provided_by=deployments)
    run("cd %(deploy_to)s/static/minify && ./minify.sh" % env)
    
@runs_once
def s3sync():
    "Sync static data with our s3 bucket"
    require("hosts", provided_by=deployments)
    run("cd %(deploy_to)s && python manage.py sync_media_s3 --gzip --force --expires" % env)
    
@runs_once
def backupdb():
    "Create a backup of the database"
    pass

@runs_once
def migratedb():
    "Migrate the database"
    require("hosts", provided_by=deployments)
    if confirm("Would you like to migrate the database?"):
        run("cd %(deploy_to)s && python manage.py migrate" % env)
    
@runs_once
def syncdb():
    "Sync the database with any new models"
    require("hosts", provided_by=deployments)
    if confirm("This script can not handle interactive shells, are you sure you want to run syncdb?"):
        run("cd %(deploy_to)s && python manage.py syncdb" % env)
    
def restart_apache():
    "Reboot Apache2 server."
    require("hosts", provided_by=deployments)
    sudo("/etc/init.d/apache2 restart")

@roles("loadbalancer")
def disable_maintenance_page():
    "Turns off the maintenance page"
    if SHOW_MAINTENANCE_PAGE:
        sudo("rm /etc/nginx/sites-enabled/maintenance")
        sudo("ln -s /etc/nginx/sites-available/rah /etc/nginx/sites-enabled/rah")
        sudo("/etc/init.d/nginx reload")
    
@runs_once
def notify_codebase():
    "Notify codebase that a new revision has been deployed"
    require("hosts", provided_by=deployments)
    match = re.search("git\@(codebasehq-deploy):(.*)\/(.*)\/(.*)\.git", env.repository)
    domain = "%s.codebasehq.com" % match.group(2)
    project = match.group(3)
    repository = match.group(4)
    username = local("git config codebase.username").strip()
    api_key = local("git config codebase.apikey").strip()
    commit_hash = local("git show-ref %(revision)s | cut -d ' ' -f 1" % env).strip()
    
    xml = []
    xml.append("<deployment>")
    xml.append("<servers>%s</servers>" % ",".join(env.hosts))
    xml.append("<revision>%s</revision>" % commit_hash)
    environment = _determine_environment()
    if environment:
        xml.append("<environment>%s</environment>" % environment)
    xml.append("<branch>%(branch)s:%(revision)s</branch>" % env)
    xml.append("</deployment>")

    url = "https://%s/%s/%s/deployments" % (domain, project, repository)
    headers = {"Content-type": "application/xml", "Accept": "application/xml", 
        "Authorization": "Basic %s" % base64.b64encode("%s:%s" % (username, api_key))}
    request = urllib2.Request(url, "".join(xml), headers)
    response = urllib2.urlopen(request).read()

def deploy(revision=None, sync_media=True):
    "Deploy code to server"
    if revision: env.revision = revision
    require("deploy_to", provided_by=deployments)
    enable_maintenance_page()
    reset()
    pull()
    checkout()
    install_requirements()
    minify()
    if bool(sync_media) and str(sync_media).upper() != "FALSE":
        s3sync()
    #backupdb()
    migratedb()
    syncdb()
    restart_apache()
    disable_maintenance_page()
    notify_codebase()
    print("%(branch)s:%(revision)s has been deployed to %(hosts)s" % env)
        