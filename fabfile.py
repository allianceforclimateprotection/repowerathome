import base64
import re
import sys
import urllib2

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.colors import green, red

env.user = "ubuntu"
env.disable_known_hosts = True

env.roledefs = {
    "application": ["ec2-184-73-88-77.compute-1.amazonaws.com"],
    "loadbalancer": ["repowerathome.com"],
    "development": ["dev.repowerathome.com"],
    "staging": ["ec2-184-72-148-152.compute-1.amazonaws.com"],
}

env.deploy_to = "/home/%(user)s/webapp" % env
env.parent = "origin"
env.revision = "HEAD"
env.repository = "git@codebasehq-deploy:rah/rah/rah.git"

def dev():
    env.roles = ["development"]
    env.environment = "development"
def staging():
    env.roles = ["staging"]
    env.environment = "staging"
def prod():
    env.roles = ["application"]
    env.environment = "production"
deployments = [dev, staging, prod]

def _query_revision(treeish="HEAD"):
    if re.match("^[0-9a-f]{40}$", treeish): return treeish
    return local("git show %s | sed q | cut -d ' ' -f 2" % treeish)
env.sha = _query_revision()

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
    if env.environment == "production":
        for host in env.roledefs["loadbalancer"]:
            with settings(host_string=host):
                sudo("rm /etc/nginx/sites-enabled/rah")
                sudo("ln -s /etc/nginx/sites-available/maintenance /etc/nginx/sites-enabled/maintenance")
                sudo("/etc/init.d/nginx reload")
    
def fetch():
    "Updates the application with new code"
    require("hosts", provided_by=deployments)
    run("cd %(deploy_to)s && git fetch --all" % env)
    
def reset():
    "Set the workspace to the desired revision"
    require("hosts", provided_by=deployments)
    run("cd %(deploy_to)s && git reset --hard" % env)
    
def checkout():
    "Checkout the revision you would like to deploy"
    require("hosts", provided_by=deployments)
    with settings(warn_only=True):
        result = run("cd %(deploy_to)s && git checkout -b \
            `date +'%%Y-%%m-%%d_%%H-%%M-%%S'`_`whoami` %(sha)s" % env)
        if result.failed:
            print(red("Have you pushed your latest changes to the repository?"))
            sys.exit(1)

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
def syncdb():
    "Sync the database with any new models"
    require("hosts", provided_by=deployments)
    if confirm("This script cannot handle interactive shells, are you sure you want to run syncdb?"):
        run("cd %(deploy_to)s && python manage.py syncdb" % env)

@runs_once
def migratedb():
    "Migrate the database"
    require("hosts", provided_by=deployments)
    if confirm("Would you like to migrate the database?"):
        run("cd %(deploy_to)s && python manage.py migrate" % env)
    
def restart_apache():
    "Reboot Apache2 server."
    require("hosts", provided_by=deployments)
    sudo("/etc/init.d/apache2 restart")

def disable_maintenance_page():
    "Turns off the maintenance page"
    if env.environment == "production":
        for host in env.roledefs["loadbalancer"]:
            with settings(host_string=host):
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
    
    xml = []
    xml.append("<deployment>")
    xml.append("<servers>%s</servers>" % ",".join(env.roles))
    xml.append("<revision>%(sha)s</revision>" % env)
    xml.append("<environment>%(environment)s</environment>" % env)
    xml.append("<branch>%(revision)s</branch>" % env)
    xml.append("</deployment>")

    url = "https://%s/%s/%s/deployments" % (domain, project, repository)
    headers = {"Content-type": "application/xml", "Accept": "application/xml", 
        "Authorization": "Basic %s" % base64.b64encode("%s:%s" % (username, api_key))}
    request = urllib2.Request(url, "".join(xml), headers)
    response = urllib2.urlopen(request).read()

def deploy(revision=None, sync_media=True, code_only=False):
    "Deploy a revision to server"
    if revision:
        env.revision = revision
        env.sha = _query_revision(revision)
    require("deploy_to", provided_by=deployments)
    #enable_maintenance_page()
    fetch()
    reset()
    checkout()
    if not code_only:
        install_requirements()
        minify()
        if bool(sync_media) and str(sync_media).upper() != "FALSE":
            s3sync()
        #backupdb()
        #syncdb()
        #migratedb()
    restart_apache()
    #disable_maintenance_page()
    notify_codebase()
    print(green("%(revision)s has been deployed to %(hosts)s" % env))