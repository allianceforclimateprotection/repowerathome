#!/usr/bin/python

"""
This script print a list of IP address for all of our servers
"""
import pprint
import boto

class AwsIps(object):
    """Prints IPs for EC2 and RDS servers"""
    def __init__(self):
        self.data = {}

    def get_ips(self):
        # Get IPs for EC2 instances
        conn = boto.connect_ec2()
        security_groups = conn.get_all_security_groups()
        for group in security_groups:
            self.data[group.name] = {}
            self.data[group.name]['private_ip_address'] = []
            self.data[group.name]['public_ip_address'] = []
            for i in group.instances():
                if i.state <> 'running':
                    continue
                self.data[group.name]['public_ip_address'].append(i.ip_address)
                self.data[group.name]['private_ip_address'].append(i.private_ip_address)

        # Get IPs for RDS instances
        conn = boto.connect_rds()
        instances = conn.get_all_dbinstances()
        for i in instances:
            self.data["db: %s" % i.id] = i.endpoint[0] if i.endpoint else "Unavailable"
        
        return self.data

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=2)
    aws = AwsIps()
    pp.pprint(AwsIps().get_ips())