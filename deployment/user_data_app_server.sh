#!/bin/bash

set -e -x
export DEBIAN_FRONTEND=noninteractive

# Copy some things to the ubuntu home folder
cp /udata/home/ubuntu/.bashrc /home/ubuntu/.bashrc
cp /udata/home/ubuntu/webapp/local_settings.py /home/ubuntu/webapp/local_settings.py

# Copy git keys
cp /udata/home/ubuntu/.ssh/config /home/ubuntu/.ssh/config
cp /udata/home/ubuntu/.ssh/deploy.pem /home/ubuntu/.ssh/deploy.pem
cp /udata/home/ubuntu/.ssh/deploy-pk.pem /home/ubuntu/.ssh/deploy-pk.pem

# Permissions
chmod 644 /home/ubuntu/.bashrc
chmod 644 /home/ubuntu/webapp/local_settings.py
chmod 644 /home/ubuntu/.ssh/config
chmod 400 /home/ubuntu/.ssh/deploy.pem
chmod 400 /home/ubuntu/.ssh/deploy-pk.pem
chown -R ubuntu:ubuntu /home/ubuntu/

# Run to undo
# sudo rm -f /home/ubuntu/.bashrc /home/ubuntu/.ssh/config /home/ubuntu/.ssh/deploy.pem /home/ubuntu/.ssh/deploy-pk.pem /home/ubuntu/webapp/local_settings.py