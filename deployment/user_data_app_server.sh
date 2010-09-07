#!/bin/bash

set -e -x
export DEBIAN_FRONTEND=noninteractive
export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'

# Copy over the apache config files
cp /udata/etc/apache2/sites-available/* /etc/apache2/sites-available/
cp /udata/etc/apache2/httpd.conf /etc/apache2/httpd.conf
cp /udata/etc/apache2/ports.conf /etc/apache2/ports.conf

# Copy some things to the ubuntu home folder
cp /udata/home/ubuntu/.bashrc /home/ubuntu/.bashrc
cp /udata/home/ubuntu/webapp/local_settings.py /home/ubuntu/webapp/local_settings.py

# Copy git keys
cp /udata/home/ubuntu/.ssh/config /home/ubuntu/.ssh/config
cp /udata/home/ubuntu/.ssh/deploy.pem /home/ubuntu/.ssh/deploy.pem
cp /udata/home/ubuntu/.ssh/deploy-pk.pem /home/ubuntu/.ssh/deploy-pk.pem

# Copy over crontab
cp /udata/etc/cron.d/send_ready_messages /etc/cron.d/send_ready_messages

# Permissions
chmod 644 /home/ubuntu/.bashrc
chmod 644 /home/ubuntu/webapp/local_settings.py
chmod 644 /home/ubuntu/.ssh/config
chmod 400 /home/ubuntu/.ssh/deploy.pem
chmod 400 /home/ubuntu/.ssh/deploy-pk.pem
chown -R ubuntu:ubuntu /home/ubuntu/

# Run to undo
# sudo rm -f /home/ubuntu/.bashrc 
# sudo rm -f /home/ubuntu/.ssh/config 
# sudo rm -f /home/ubuntu/.ssh/deploy.pem 
# sudo rm -f /home/ubuntu/.ssh/deploy-pk.pem 
# sudo rm -f /home/ubuntu/webapp/local_settings.py
# sudo rm -f /etc/cron.d/send_ready_messages