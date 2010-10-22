import boto
import os
import re
import tempfile
import time

from boto.ec2.address import Address
from fabric.api import env, settings, local, run, sudo, put, hide
from fabric.contrib.console import confirm

env.disable_known_hosts = True

env.zone = "us-east-1b"
env.key_name = "acp-ec2"

AMIs = {
    "ubuntu-10.04-32": "ami-6c06f305",
    "ubuntu-10.10-32": "ami-508c7839",
}

env.aws_key = local("echo $RAH_AWS_ACCESS_KEY")
env.aws_secret = local("echo $RAH_AWS_SECRET_KEY")
env.ec2_conn = boto.connect_ec2(env.aws_key, env.aws_secret)

def _security_groups():
    "Add a list of available security groups to the environment"
    return dict([(sg.name, sg) for sg in env.ec2_conn.get_all_security_groups()])
env.security_groups = _security_groups()

def _associate_ip(instance, ip):
    address = Address(instance.connection, ip)
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
    return launched_image
    
def _wait_for_instance(instance, check_increment=5):
    while instance.update() != "running":
        time.sleep(check_increment)
        print "%s is %s" % (instance, instance.state)
    with settings(hide("running", "warnings", "stderr"), warn_only=True):
        while local("ssh -o StrictHostKeyChecking=no ubuntu@%s 'echo TEST'" % instance.public_dns_name).failed:
            time.sleep(check_increment)
            print "%s is %s" % (instance, instance.state)
        
def _bootstrap(script):
    remote_script = "~/%s" % os.path.basename(script)
    parent_dir = os.path.dirname(os.path.abspath(script))
    contents = re.sub("::(.*)::", lambda x: open("%s/%s" % (parent_dir, x.group(1))).read().replace("$", "\$"),
        open(script).read())
    temp = tempfile.NamedTemporaryFile(delete=True)
    temp.write(contents)
    temp.flush()
    put(temp.name, remote_script)
    temp.close()
    sudo("export AWS_ACCESS_KEY=%s && export AWS_SECRET_KEY=%s && export PUBLIC_DNS_NAME=%s &&\
        bash %s" % (env.aws_key, env.aws_secret, env.host_string, remote_script))
    run("rm %s" % remote_script)
    
def boot_test():
    env.host_string = "ec2-184-73-45-17.compute-1.amazonaws.com"
    _bootstrap("fabfile/bootstrap.sh")

def launch_server(name="test", instance_type="t1.micro", ami=AMIs["ubuntu-10.10-32"], 
        bootstrap_script="fabfile/bootstrap.sh"):
    "launch a new server"
    instance = _launch_ec2_ami(ami, instance_type=instance_type, security_groups=(
        env.security_groups["ssh_access"], env.security_groups["load_balancers"],
        env.security_groups["app_servers"])).instances[0]
    _wait_for_instance(instance)
    instance.add_tag(key="Name", value=name)
    with settings(host_string=instance.public_dns_name):
        _bootstrap(bootstrap_script)

def launch_cloud(count=1, lb_type="m1.small", app_type="c1.medium", rds_type="db.m1.small"):
    "launch a new cloud (loadbalancer, appserver(s) and RDS)"
    launch_loadbalancer(instance_type=lb_type)
    launch_appservers(count=count, instance_type=app_type)
    launch_rds(instance_type=rds_type)
    
def launch_loadbalancer(instance_type="m1.small", ami=AMIs["ubuntu-10.04-32"]):
    "Start up a new load balancer server"
    instance = _launch_ec2_ami(ami, instance_type=instance_type, security_groups=(
        env.security_groups["ssh_access"], env.security_groups["load_balancers"])).instances[0]
    return instance
        
def launch_appservers(count=1, instance_type="c1.medium", ami=AMIs["ubuntu-10.04-32"]):
    "Start up a set of new app servers"
    instances = _launch_ec2_ami(ami, min_count=count, max_count=count, instance_type=instance_type,
        security_groups=(env.security_groups["ssh_access"], env.security_groups["app_servers"]),
        ).instances
    return instances
        
def launch_rds(id="staging", instance_type="db.m1.small", size="5"):
    "Start up a new RDS"
    return boto.connect_rds().create_dbinstance(id=id, allocated_storage=size, instance_class=instance_type,
        master_username="rah_db_user", master_password="", db_name="rah", security_groups=["default"],
        availability_zone=env.zone, preferred_maintenance_window="Sun:10:00-Sun:14:00",
        preferred_backup_window="08:00-10:00")
    
