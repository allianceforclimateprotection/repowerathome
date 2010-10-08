#!/bin/bash

set -e -x
export DEBIAN_FRONTEND=noninteractive
export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'

# Copy nginx sites over
cp /udata/etc/nginx/sites-available/* /etc/nginx/sites-available/
cp /udata/etc/nginx/nginx.conf /etc/nginx/nginx.conf

# Copy SSL keys and certs into the proper locations
cp /udata/etc/ssl/repowerathome.key /etc/ssl/repowerathome.key
cp /udata/etc/ssl/private/repowerathome.csr /etc/ssl/private/repowerathome.csr
cp /udata/etc/ssl/private/repowerathome.key /etc/ssl/private/repowerathome.key
cp /udata/etc/ssl/private/repowerathome_with_pass.key /etc/ssl/private/repowerathome_with_pass.key
cp /udata/etc/ssl/certs/repowerathome.crt /etc/ssl/certs/repowerathome.crt
cp /udata/etc/ssl/certs/repowerathome_with_gd_bundle.crt /etc/ssl/certs/repowerathome_with_gd_bundle.crt

# Copy some things to the ubuntu home folder
cp /udata/home/ubuntu/.bashrc /home/ubuntu/.bashrc
cp /udata/home/ubuntu/htpasswd /home/ubuntu/htpasswd

# Copy git keys
cp /udata/home/ubuntu/.ssh/config /home/ubuntu/.ssh/config
cp /udata/home/ubuntu/.ssh/deploy.pem /home/ubuntu/.ssh/deploy.pem
cp /udata/home/ubuntu/.ssh/deploy-pk.pem /home/ubuntu/.ssh/deploy-pk.pem

# Permissions
chmod 644 /home/ubuntu/htpasswd
chmod 644 /home/ubuntu/.bashrc
chmod 644 /home/ubuntu/.ssh/config
chmod 400 /home/ubuntu/.ssh/deploy.pem
chmod 400 /home/ubuntu/.ssh/deploy-pk.pem
chown -R ubuntu:ubuntu /home/ubuntu/

# Run updates
sudo aptitude update
sudo aptitude safe-upgrade -y

# Use this command to undo it all before making an AMI
# sudo rm -f /etc/ssl/repowerathome.key 
# sudo rm -f /etc/ssl/private/repowerathome.csr 
# sudo rm -f /etc/ssl/private/repowerathome.key 
# sudo rm -f /etc/ssl/private/repowerathome_with_pass.key 
# sudo rm -f /etc/ssl/certs/repowerathome.crt 
# sudo rm -f /etc/ssl/certs/repowerathome_with_gd_bundle.crt 
# sudo rm -f /home/ubuntu/htpasswd 
# sudo rm -f /home/ubuntu/.bashrc 
# sudo rm -f /home/ubuntu/.ssh/config 
# sudo rm -f /home/ubuntu/.ssh/deploy.pem 
# sudo rm -f /home/ubuntu/.ssh/deploy-pk.pem