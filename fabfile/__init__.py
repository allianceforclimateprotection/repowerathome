from fabric.api import env, settings, local, run, abort
from fabric.contrib.console import confirm

from utils import query_revision

env.user = "ubuntu"
env.disable_known_hosts = True

env.roledefs = {
    "application": ["ec2-75-101-252-146.compute-1.amazonaws.com", "ec2-50-16-73-62.compute-1.amazonaws.com"],
    "loadbalancer": ["repowerathome.com"],
    "staging": ["staging.repowerathome.com"],
}

env.deploy_to = "/home/%(user)s/webapp" % env
env.parent = "origin"
env.revision = "HEAD"
env.sha = query_revision(env.revision)
env.repository = "git@codebasehq.com:rah/rah/rah.git"

def staging():
    env.roles = ["staging"]
    env.environment = "staging"
    env.loadbalancers = env.roledefs["staging"]

def prod():
    env.roles = ["application"]
    env.environment = "production"
    env.loadbalancers = env.roledefs["loadbalancer"]

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
from server import *
