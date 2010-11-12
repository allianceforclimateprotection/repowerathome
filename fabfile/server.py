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

from deploy import install_requirements

env.disable_known_hosts = True

env.zone = "us-east-1b"
env.key_name = "acp-ec2"

env.db_name = "rah"
env.db_user = "rah_db_user"

AMIs = {
    "ubuntu-10.10-32": "ami-b61de9df",
    "ubuntu-10.10-64": "ami-548c783d",
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
    kwargs["placement"] = env.zone
    user_data_file = kwargs.pop("user_data_file", None)
    if user_data_file:
        kwargs["user_data"] = open(user_data_file, "r").read()
    launched_image = env.ec2_conn.get_image(ami).run(key_name=env.key_name, **kwargs)
    time.sleep(4)
    return launched_image
    
def _wait_for_resources(resources, check_increment=5, up_state="running", test_ssh=True):
    while any([r.update() != up_state for r in resources]):
        time.sleep(check_increment)
        print ", ".join(["%s is %s" % (r, r.state) for r in resources])
    if test_ssh:
        with settings(hide("running", "warnings", "stderr"), warn_only=True):
            while any([local("ssh -o StrictHostKeyChecking=no ubuntu@%s 'echo TEST'" % r.public_dns_name).failed for r in resources]):
                time.sleep(check_increment)
                print ", ".join(["%s is %s" % (r, r.state) for r in resources])
        
def _bootstrap(shell_vars=None, command="bootstrap_system;", script=DEFAULT_BOOTSTRAP_SCRIPT):
    remote_script = "~/%s" % os.path.basename(script)
    parent_dir = os.path.dirname(os.path.abspath(script))
    contents = re.sub("::(.*)::", lambda x: open("%s/%s" % (parent_dir, x.group(1))).read().replace("$", "\$"),
        open(script).read()) # the bootstrap script needs to be filled with external file contents
    temp = tempfile.NamedTemporaryFile(delete=True)
    temp.write(contents)
    temp.flush()
    put(temp.name, remote_script)
    temp.close()
    var_exports = " && ".join(['export %s="%s"' % (k,v) for k,v in shell_vars.items()])
    sudo("%s && echo '. %s; %s' | bash" % (var_exports, remote_script, command))
    run("rm %s" % remote_script)
    
def _print_mysqlduplicate_alias(name, db_password, servers, host="127.0.0.1"):
    print(green("""
        "%s": {
            "SERVER": "%s@%s",
            "DATABASE": "%s",
            "HOST": "%s",
            "USER": "%s",
            "PASSWORD": "%s",
            "CAN_REPLACE": True,
        },""" % (name, env.user, servers[0], env.db_name, host, env.db_user, db_password)))
    print(green("Add the above setting to your local_settings module and execute:"))
    print(green("\t./mysqlduplicate.py prod %s" % name))
    print(green("Add the following to your fabfile/__init__.py:"))
    print(green('\t "%s": %s,' % (name, servers)))
    print(green("Finally, execute:"))
    print(green("\tfab -H %s syncdb [this might not work yet]" % server))
    print(green("\tfab -H %s restart_app_server" % server))
    
def launch_server(environment="staging", instance_type="t1.micro", ami=AMIs["ubuntu-10.10-64"], 
    tag_name=None):
    "launch a new server"
    tag_name = tag_name.replace(" ", "-") if tag_name else None
    name = tag_name or environment
    instance = _launch_ec2_ami(ami, instance_type=instance_type, security_groups=(
        env.security_groups["ssh_access"], env.security_groups["load_balancers"],
        env.security_groups["app_servers"])).instances[0]
    _wait_for_resources([instance])
    instance.add_tag(key="Name", value="%s" % tag_name if tag_name else environment)
    with settings(host_string=instance.public_dns_name):
        db_password = _generate_password()
        shell_vars = { "AWS_ACCESS_KEY": env.aws_key, "AWS_SECRET_KEY": env.aws_secret, 
            "PUBLIC_DNS_NAME": instance.public_dns_name, "APP_SERVER_IPS": instance.private_ip_address,
            "DB_PASSWORD": db_password, "ENVIRONMENT": environment, "DB_NAME": env.db_name,
            "DB_USER": env.db_user }
        _bootstrap(shell_vars=shell_vars, 
            command="bootstrap_system; bootstrap_database; bootstrap_appserver; bootstrap_loadbalancer;")
        install_requirements()
    _print_mysqlduplicate_alias(name, db_password, [instance.public_dns_name])

def launch_cloud(environment="staging", count=1, lb_type="t1.micro", app_type="t1.micro", 
        rds_type="db.m1.small", ami=AMIs["ubuntu-10.10-64"], tag_name=None):
    "launch a new cloud (loadbalancer, appserver(s) and RDS)"
    tag_name = tag_name.replace(" ", "-") if tag_name else None
    name = tag_name or environment
    rds, rds_endpoint, db_password = _launch_rds(id=name, instance_type=rds_type)
    app_servers = _launch_appservers(db_password, rds_endpoint, name=name, environment=environment,
        count=count, instance_type=app_type, ami=ami)
    lb_server = _launch_loadbalancer([s.private_ip_address for s in app_servers], name=name, 
        environment=environment, instance_type=lb_type, ami=ami)
    _print_mysqlduplicate_alias(name, db_password, [a.public_dns_name for a in app_servers], host=rds_endpoint)
    
def grow_cloud(cloud_name):
    server = None;
    for r in env.ec2_conn.get_all_instances():
        i = r.instances[0]
        if "Master App Server" in i.tags and "Cloud" in i.tags and i.tags["Cloud"] == cloud_name:
            server = i
            break
    if not server:
        abort(red("No master app server in %s can be found." % cloud_name))
    return _duplicate_appserver(id=server.id, name=cloud_name, count=1)
    
def _launch_rds(id="staging", instance_type="db.m1.small", size="5"):
    "Start up a new RDS, returns a 3-tuple - (RDS, RDS Endpoint, DB Password)"
    db_password = _generate_password()
    rds_endpoint = rds_endpoint = "%s.co6ulcbqxe1u.us-east-1.rds.amazonaws.com" % id
    rds = env.rds_conn.create_dbinstance(id=id, allocated_storage=size, instance_class=instance_type,
        master_username=env.db_user, master_password=db_password, db_name=env.db_name, security_groups=["default"],
        param_group="rah", availability_zone=env.zone, preferred_maintenance_window="Sun:10:00-Sun:14:00",
        preferred_backup_window="08:00-10:00", backup_retention_period=7)
    return (rds, rds_endpoint, db_password)
        
def _launch_appservers(db_password, db_host, name="staging", environment="staging", count=1, 
    instance_type="t1.micro", ami=AMIs["ubuntu-10.10-64"]):
    "Start up a set of new app servers"
    count = int(count)
    server = _launch_ec2_ami(ami, min_count=1, max_count=1, instance_type=instance_type,
        security_groups=(env.security_groups["ssh_access"], env.security_groups["app_servers"])).instances[0]
    _wait_for_resources([server])
    with settings(host_string=server.public_dns_name):
        shell_vars = { "AWS_ACCESS_KEY": env.aws_key, "AWS_SECRET_KEY": env.aws_secret, 
            "PUBLIC_DNS_NAME": server.public_dns_name, 
            "DB_PASSWORD": db_password, "ENVIRONMENT": environment, "DB_NAME": env.db_name,
            "DB_USER": env.db_user, "DB_HOST": db_host }
        _bootstrap(shell_vars=shell_vars, command="bootstrap_system; bootstrap_appserver;")
        server.add_tag(key="Master App Server", value="True")
        server.add_tag(key="Name", value="%s appserver" % name)
        server.add_tag(key="Cloud", value=name)
    servers = [server]
    if count > 1:
        servers = servers + _duplicate_appserver(id=server.id, name=name, count=count-1)
    return servers
    
def _duplicate_appserver(id, name, count=1):
    image_id = env.ec2_conn.create_image(id, "%s appserver" % name, no_reboot=True)
    image = env.ec2_conn.get_image(image_id)
    _wait_for_resources([image], up_state="available", test_ssh=False)
    servers = _launch_ec2_ami(image_id, min_count=count, max_count=count, 
        instance_type=instance_type, security_groups=(env.security_groups["ssh_access"], 
        env.security_groups["app_servers"])).instances
    _wait_for_resources(servers)
    for s in servers:
        s.add_tag(key="Name", value="%s appserver" % name)
        s.add_tag(key="Cloud", value=name)
    return servers
    
def _launch_loadbalancer(app_server_ips, name="staging", environment="staging", instance_type="t1.micro",
    ami=AMIs["ubuntu-10.10-64"]):
    "Start up a new load balancer server"
    server = _launch_ec2_ami(ami, instance_type=instance_type, security_groups=(
        env.security_groups["ssh_access"], env.security_groups["load_balancers"])).instances[0]
    _wait_for_resources([server])
    with settings(host_string=server.public_dns_name):
        shell_vars = { "AWS_ACCESS_KEY": env.aws_key, "AWS_SECRET_KEY": env.aws_secret, 
            "PUBLIC_DNS_NAME": server.public_dns_name, 
            "APP_SERVER_IPS": " ".join([ip for ip in app_server_ips]) }
        _bootstrap(shell_vars, command="bootstrap_system; bootstrap_loadbalancer;")
    server.add_tag(key="Name", value="%s loadbalancer" % name)
    server.add_tag(key="Cloud", value=name)
    return server
