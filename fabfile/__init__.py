from fabric.api import env, settings, local, run, abort
from fabric.contrib.console import confirm

from utils import query_revision

env.user = "ubuntu"
env.disable_known_hosts = True

env.roledefs = {
    "application": ["ec2-184-73-88-77.compute-1.amazonaws.com"],
    "loadbalancer": ["repowerathome.com"],
    "staging": ["ec2-184-72-148-152.compute-1.amazonaws.com"],
}

env.deploy_to = "/home/%(user)s/webapp" % env
env.parent = "origin"
env.revision = "HEAD"
env.sha = query_revision(env.revision)
env.repository = "git@codebasehq-deploy:rah/rah/rah.git"

def staging():
    env.roles = ["staging"]
    env.environment = "staging"
def prod():
    env.roles = ["application"]
    env.environment = "production"
deployments = [staging, prod]

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
        
from codebase import *
from deploy import *