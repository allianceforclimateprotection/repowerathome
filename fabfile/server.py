import boto
import os
import random
import re
import string
import tempfile
import time

from fabric.api import env, settings, local, run, sudo, put, hide, abort
from fabric.contrib.console import confirm
from fabric.colors import green, red

from deploy import install_requirements, restart_apache

env.disable_known_hosts = True

env.zone = "us-east-1b"
env.key_name = "acp-ec2"

env.db_name = "rah"
env.db_user = "rah_db_user"

AMIs = {
    "ubuntu-10.10-32": "ami-b61de9df",
}

env.aws_key = local("echo $RAH_AWS_ACCESS_KEY")
env.aws_secret = local("echo $RAH_AWS_SECRET_KEY")
if not (env.aws_key and env.aws_secret):
    abort(red("You must set RAH_AWS_ACCESS_KEY and RAH_AWS_SECRET_KEY in your environment."))
env.ec2_conn = boto.connect_ec2(env.aws_key, env.aws_secret)
env.rds_conn = boto.connect_rds(env.aws_key, env.aws_secret)

DEFAULT_BOOTSTRAP_SCRIPT = "fabfile/bootstrap.sh"
DEFAULT_USER_DATA_FILE = "fabfile/user_data.sh"

def _security_groups():
    "Add a list of available security groups to the environment"
    return dict([(sg.name, sg) for sg in env.ec2_conn.get_all_security_groups()])
env.security_groups = _security_groups()

def _generate_password(length=36):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)])

def _associate_ip(instance, ip):
    address = boto.ec2.address.Address(instance.connection, ip)
    if address.instance_id:
        if not confirm("%s is already associated with %s, are you sure you want to do this?"):
            return
        address.disassociate()
    address.associate(instance.id)
    
def _launch_ec2_ami(ami, *args, **kwargs):
    if kwargs["instance_type"] != "t1.micro":
        kwargs["placement_group"] = env.zone
    user_data_file = kwargs.pop("user_data_file", None)
    if user_data_file:
        kwargs["user_data"] = open(user_data_file, "r").read()
    launched_image = env.ec2_conn.get_image(ami).run(key_name=env.key_name, **kwargs)
    time.sleep(4)
    return launched_image
    
def _wait_for_instances(instances, check_increment=5, test_ssh=True):
    while any([i.update() != "running" for i in instances]):
        time.sleep(check_increment)
        print ", ".join(["%s is %s" % (i, i.state) for i in instances])
    if test_ssh:
        with settings(hide("running", "warnings", "stderr"), warn_only=True):
            while any([local("ssh -o StrictHostKeyChecking=no ubuntu@%s 'echo TEST'" % i.public_dns_name).failed for i in instances]):
                time.sleep(check_increment)
                print ", ".join(["%s is %s" % (i, i.state) for i in instances])
        
def _bootstrap(script, shell_vars=None, command="bootstrap_system;"):
    remote_script = "~/%s" % os.path.basename(script)
    parent_dir = os.path.dirname(os.path.abspath(script))
    contents = re.sub("::(.*)::", lambda x: open("%s/%s" % (parent_dir, x.group(1))).read().replace("$", "\$"),
        open(script).read()) # the bootstrap script needs to be filled with external file contents
    temp = tempfile.NamedTemporaryFile(delete=True)
    temp.write(contents)
    temp.flush()
    put(temp.name, remote_script)
    temp.close()
    var_exports = " && ".join(["export %s=%s" % (k,v) for k,v in shell_vars.items()])
    sudo("%s && echo '. %s; %s' | bash" % (var_exports, remote_script, command))
    run("rm %s" % remote_script)
    
def _print_mysqlduplicate_alias(environment, db_password, server, host="127.0.0.1"):
    print(green("""
        "%s": {
            "SERVER": "%s@%s",
            "DATABASE": "%s",
            "HOST": "%s",
            "USER": "%s",
            "PASSWORD": "%s",
            "CAN_REPLACE": True,
        },""" % (environment, env.user, server, env.db_name, host, env.db_user, db_password)))
    print(green("Add the above setting to your local_settings module and execute:"))
    print(green("\t./mysqlduplicate.py prod %s" % environment))
    print(green("\tfab -H %s syncdb [this might not work yet]" % server))
    print(green("\tfab -H %s restart_apache" % server))
    
def launch_server(environment="staging", instance_type="t1.micro", ami=AMIs["ubuntu-10.10-32"], 
        bootstrap_script=DEFAULT_BOOTSTRAP_SCRIPT):
    "launch a new server"
    instance = _launch_ec2_ami(ami, instance_type=instance_type, security_groups=(
        env.security_groups["ssh_access"], env.security_groups["load_balancers"],
        env.security_groups["app_servers"])).instances[0]
    _wait_for_instances([instance])
    instance.add_tag(key="Name", value="%s server" % environment)
    with settings(host_string=instance.public_dns_name):
        db_password = _generate_password()
        shell_vars = { "AWS_ACCESS_KEY": env.aws_key, "AWS_SECRET_KEY": env.aws_secret, 
            "PUBLIC_DNS_NAME": instance.public_dns_name, "APP_SERVER_IPS": instance.private_ip_address,
            "DB_PASSWORD": db_password, "ENVIRONMENT": environment, "DB_NAME": env.db_name,
            "DB_USER": env.db_user }
        _bootstrap(bootstrap_script, shell_vars, 
            command="bootstrap_system; bootstrap_database; bootstrap_appserver; bootstrap_loadbalancer;")
        install_requirements()
    _print_mysqlduplicate_alias(environment, db_password, instance.public_dns_name)

def launch_cloud(environment="staging", count=1, lb_type="t1.micro", app_type="t1.micro", 
        rds_type="db.m1.small", ami=AMIs["ubuntu-10.10-32"], 
        bootstrap_script=DEFAULT_BOOTSTRAP_SCRIPT):
    "launch a new cloud (loadbalancer, appserver(s) and RDS)"
    db_password = _generate_password()
    rds = _launch_rds(db_password=db_password, id=environment, instance_type=rds_type)
    rds_endpoint = "%s.co6ulcbqxe1u.us-east-1.rds.amazonaws.com" % environment
    app_servers = _launch_appservers(count=count, instance_type=app_type, ami=ami)
    lb_server = _launch_loadbalancer(instance_type=lb_type, ami=ami)
    _wait_for_instances(app_servers)
    for i in app_servers:
        i.add_tag(key="Name", value="%s appserver" % environment)
    for server in app_servers:
        with settings(host_string=server.public_dns_name):
            shell_vars = { "AWS_ACCESS_KEY": env.aws_key, "AWS_SECRET_KEY": env.aws_secret, 
                "PUBLIC_DNS_NAME": server.public_dns_name, 
                "DB_PASSWORD": db_password, "ENVIRONMENT": environment, "DB_NAME": env.db_name,
                "DB_USER": env.db_user, "DB_HOST": rds_endpoint }
            _bootstrap(bootstrap_script, shell_vars, command="bootstrap_system; bootstrap_appserver;")
            install_requirements()
    _wait_for_instances([lb_server])
    lb_server.add_tag(key="Name", value="%s loadbalancer" % environment)
    with settings(host_string=lb_server.public_dns_name):
        shell_vars = { "AWS_ACCESS_KEY": env.aws_key, "AWS_SECRET_KEY": env.aws_secret, 
            "PUBLIC_DNS_NAME": lb_server.public_dns_name, 
            "APP_SERVER_IPS": " ".join([i.private_ip_address for i in app_servers]) }
        _bootstrap(bootstrap_script, shell_vars, command="bootstrap_system; bootstrap_loadbalancer;")
    _print_mysqlduplicate_alias(environment, db_password, app_servers[0].public_dns_name, host=rds_endpoint)
    
def _launch_rds(db_password, id="staging", instance_type="db.m1.small", size="5"):
    "Start up a new RDS"
    return env.rds_conn.create_dbinstance(id=id, allocated_storage=size, instance_class=instance_type,
        master_username=env.db_user, master_password=db_password, db_name=env.db_name, security_groups=["default"],
        param_group="rah", availability_zone=env.zone, preferred_maintenance_window="Sun:10:00-Sun:14:00",
        preferred_backup_window="08:00-10:00", backup_retention_period=7)
        
def _launch_appservers(count=1, instance_type="c1.medium", ami=AMIs["ubuntu-10.10-32"]):
    "Start up a set of new app servers"
    return _launch_ec2_ami(ami, min_count=count, max_count=count, instance_type=instance_type,
        security_groups=(env.security_groups["ssh_access"], env.security_groups["app_servers"])).instances
    
def _launch_loadbalancer(instance_type="m1.small", ami=AMIs["ubuntu-10.10-32"]):
    "Start up a new load balancer server"
    return _launch_ec2_ami(ami, instance_type=instance_type, security_groups=(
        env.security_groups["ssh_access"], env.security_groups["load_balancers"])).instances[0]