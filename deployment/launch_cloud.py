#!/usr/bin/python

import os
import string
from random import choice
from time import sleep

import boto

class CloudMaker(object):
    """docstring for CloudMaker"""
    def __init__(self):
        self.conf = {
            "load_balancers": {
                "ami": "ami-c28862ab",
                "instance_type": "m1.small",
                "user_data_script": "user_data_load_balancer.sh"
            },
            "app_servers": {
                "ami": "ami-60957f09",
                "instance_type": "c1.medium",
                "user_data_script": "user_data_app_server.sh",
                "number": 1,
                "twit_key": "bfFELg3eHpBpku4NeGik4A",
                "twit_secret": "GXclDdMAKmaaXaO8nnx1G6SKxtYqBOeefoKhaqLVy50",
                "fb_appid": "125979060778877",
                "fb_secret": "16b5593ed80686a835c9b0cb9e9fbaad",
                "postmark_key": "eea375a8-32a2-4786-bce8-8f958ab79986"
            },
            "db_server": {
                "instance_type": "db.m1.small",
                "db_size": "5",
                "user": "rah_db_user",
                "name": "rah"
            },
            "udata": "snap-6a9f1e01",
            "zone": "us-east-1b",
            "s3_bucket": "staging.static.repowerathome.com"
        }
        
        # Prod settings
        # "twit_key": "haEAyyAy4WQZe6o8JScIlA",
        # "twit_secret": "Sx7i5kTzkdnatjGGLqL9G8u93yTmzZE6ZkckIQ",
        # "fb_appid": "132085630163980",
        # "fb_secret": "4beec8948183fb70c283bb6b0571d7a2",
        
        # Connections
        self.ec2_conn = boto.connect_ec2()
        self.rds_conn = boto.connect_rds()
        self.s3_conn = boto.connect_s3()
        # Server Instances
        self.load_balancer = None
        self.app_servers = []
        self.db_server = None
        # udata volumes
        self.lb_udata = None
        self.app_udata = []
        # Generated DB params
        self.db_pass = ''.join([choice(string.ascii_letters + string.digits) for i in range(36)])
        self.db_id = 'a' + ''.join([choice(string.letters + string.digits) for i in range(8)])
        # S3 info
        self.s3_bucket = None
        self.s3_bucket_url = None
        
    def create_udata_volumes(self):
        # Create udata volumes for load balancer
        self.lb_udata = self.ec2_conn.create_volume(1, self.conf["zone"], snapshot=self.conf["udata"])
        
        # Create udata volumes for app servers
        for i in range(int(self.conf['app_servers']['number'])):
            self.app_udata.append(self.ec2_conn.create_volume(1, self.conf["zone"], snapshot=self.conf["udata"]))
    
    def lauch_db_server(self):
        # Launch DB instance
        self.db_server = self.rds_conn.create_dbinstance(
            id = self.db_id, 
            allocated_storage = self.conf['db_server']['db_size'], 
            instance_class = self.conf['db_server']['instance_type'],
            master_username = self.conf['db_server']['user'], 
            master_password = self.db_pass, 
            port=3306,
            engine='MySQL5.1', 
            db_name=self.conf['db_server']['name'], 
            param_group="rah",
            security_groups=["default"],
            availability_zone=self.conf['zone'],
            preferred_maintenance_window='Sun:10:00-Sun:14:00',
            backup_retention_period=7,
            preferred_backup_window="08:00-10:00",
            multi_az=False
        )
        print "Launched DB instance!"

    def lauch_load_balancer(self):
        # Bring up load balancers
        self.load_balancer  = self.ec2_conn.get_image(self.conf["load_balancers"]["ami"]).run(
            min_count       = 1, 
            max_count       = 1, 
            key_name        = "acp-ec2", 
            security_groups = self.ec2_conn.get_all_security_groups(groupnames=['ssh_access', 'load_balancers']), 
            user_data       = open(self.conf["load_balancers"]["user_data_script"], 'r').read(), 
            instance_type   = self.conf["load_balancers"]["instance_type"], 
            placement       = self.conf["zone"]
        ).instances[0]
        print "Launced load balancer!"
    
    def launch_app_servers(self):
        # Launch app servers
        self.app_servers = self.ec2_conn.get_image(self.conf["app_servers"]["ami"]).run(
            min_count       = self.conf['app_servers']['number'], 
            max_count       = self.conf['app_servers']['number'], 
            key_name        = "acp-ec2", 
            security_groups = self.ec2_conn.get_all_security_groups(groupnames=['ssh_access', 'app_servers']), 
            user_data       = open(self.conf["app_servers"]["user_data_script"], 'r').read(), 
            instance_type   = self.conf["app_servers"]["instance_type"], 
            placement       = self.conf["zone"]
        ).instances
        print "Launched %s app server(s)!" % self.conf['app_servers']['number']
        
        # Give amazon a few seconds to catch up before we start monitoring
        sleep(5)

    def monitor_instances(self):
        self.load_balancer.update()
        self.db_server = self.rds_conn.get_all_dbinstances(instance_id=self.db_server.id)[0]
        status_list = [
            ('Load Balancer', self.load_balancer.state, self.load_balancer.state == 'running',),
            ('DB Server', self.db_server.status, self.db_server.status == 'available',)
        ]            
        for i in self.app_servers:
            i.update()
            status_list.append(('App Server', i.state, i.state == 'running',))
        
        all_ready = True
        status_summary = ""
        for server, status, ready in status_list:
            if not ready:
                all_ready = False
            status_summary += "%s: %s    " % (server, status)
        
        return (all_ready, status_summary,)
    
    def attach_udata_volumes(self):
        # Attach udata volume to load balancer
        self.ec2_conn.attach_volume(self.lb_udata.id, self.load_balancer.id, "/dev/sdp")
        
        # Attach udata volumes to all the app servers and update their vhost files
        for i in range(int(self.conf['app_servers']['number'])):
            self.ec2_conn.attach_volume(self.app_udata[i].id, self.app_servers[i].id, "/dev/sdp")
    
    def set_s3_bucket(self):
        # If there's a bucket specified in the conf, just use that
        if self.conf['s3_bucket']:
            self.s3_bucket = self.s3_conn.get_bucket(self.conf['s3_bucket'])
        # Otherwise, create a new bucket for this cloud
        else:
            self.s3_bucket = self.s3_conn.create_bucket('rah-%s' % self.load_balancer.public_dns_name)
            self.s3_bucket.make_public()

        print "S3 bucket set! (%s)" % self.s3_bucket.name

        # Set the bucket URL
        if self.s3_bucket.name == "prod.static.repowerathome.com":
            self.s3_bucket_url = "http://prod.static.repowerathome.com"
        elif self.s3_bucket.name == "staging.static.repowerathome.com":
            self.s3_bucket_url = "http://staging.static.repowerathome.com"
        else:
            self.s3_bucket_url = "http://s3.amazonaws.com/%s/" % self.s3_bucket.name
        
    def run_commands(self):        
        # Create a list of app server IPs to pass to a command
        server_list = ""
        for i in self.app_servers:
            server_list += "server %s:8080;" % i.private_ip_address
        
        # List of commands to run on the load balancers
        lb_commands = [
            "sudo sed -i 's/_public_dns_name/%s/' /etc/nginx/sites-available/rah" % self.load_balancer.public_dns_name,
            "sudo sed -i 's/_public_dns_name/%s/' /etc/nginx/sites-available/maintenance" % self.load_balancer.public_dns_name,
            "sudo sed -i 's/_upstream_servers;/%s/' /etc/nginx/sites-available/rah" % server_list,
            "sudo /etc/init.d/nginx restart"
        ]
        for command in lb_commands:
            print command
            while os.system('ssh ubuntu@%s "%s"' % (self.load_balancer.public_dns_name, command)) <> 0:
                sleep(3)        
        
        # List of commands to run on the app servers
        app_commands = [
            "sudo sed -i 's/_public_dns_name/%s/' /etc/apache2/sites-available/rah" % self.load_balancer.public_dns_name,
            "sudo sed -i 's/_db_name/%s/' /home/ubuntu/webapp/local_settings.py" % self.conf['db_server']['name'],
            "sudo sed -i 's/_db_user/%s/' /home/ubuntu/webapp/local_settings.py" % self.conf['db_server']['user'],
            "sudo sed -i 's/_db_pass/%s/' /home/ubuntu/webapp/local_settings.py" % self.db_pass,
            "sudo sed -i 's/_db_host/%s/' /home/ubuntu/webapp/local_settings.py" % self.db_server.endpoint[0],
            "sudo sed -i 's/_db_port/%s/' /home/ubuntu/webapp/local_settings.py" % self.db_server.endpoint[1],
            "sudo sed -i 's/_twit_key/%s/' /home/ubuntu/webapp/local_settings.py" % self.conf['app_servers']['twit_key'],
            "sudo sed -i 's/_twit_secret/%s/' /home/ubuntu/webapp/local_settings.py" % self.conf['app_servers']['twit_secret'],
            "sudo sed -i 's/_fb_appid/%s/' /home/ubuntu/webapp/local_settings.py" % self.conf['app_servers']['fb_appid'],
            "sudo sed -i 's/_fb_secret/%s/' /home/ubuntu/webapp/local_settings.py" % self.conf['app_servers']['fb_secret'],
            "sudo sed -i 's/_s3_bucket/%s/' /home/ubuntu/webapp/local_settings.py" % self.s3_bucket.name,
            "sudo sed -i 's|_media_url|%s|' /home/ubuntu/webapp/local_settings.py" % self.s3_bucket_url,
            "sudo sed -i 's/_postmark_key/%s/' /home/ubuntu/webapp/local_settings.py" % self.conf['app_servers']['postmark_key'],
            "sudo /etc/init.d/apache2 restart"    
        ]
        for command in app_commands:
            print command
            for i in self.app_servers:
                while os.system('ssh ubuntu@%s "%s"' % (i.public_dns_name, command)) <> 0:
                    sleep(3)
    
    def print_ips(self):
        print ""
        print "===================================================="
        print "Load Balancer: %s" % self.load_balancer.public_dns_name
        print "App Servers: %s" % ", ".join([i.public_dns_name for i in self.app_servers])
        print "DB Server: %s" % self.db_server.endpoint[0]
        print "S3 Bucket URL %s: " % self.s3_bucket_url
        print ""
        print ""
    
    def main(self):
        self.create_udata_volumes()
        self.lauch_db_server()
        self.lauch_load_balancer()
        self.launch_app_servers()
        
        # Wait till all the instances are ready
        while True:
            all_ready, status = self.monitor_instances()
            print status
            if all_ready:
                break
            else:
                sleep(5)
        
        self.attach_udata_volumes()
        self.set_s3_bucket()
        self.run_commands()
        self.print_ips()
        
if __name__ == "__main__":
    CloudMaker().main()
