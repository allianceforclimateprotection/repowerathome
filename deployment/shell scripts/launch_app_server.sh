#!/bin/bash

# This script launches a new App Server

# Set this variable to the load balancer AMI
AMI=ami-22a14b4b

# Set this variable to an EBS snapshot containing user data
UDATA_SNAPSHOT=snap-62923409

ec2-run-instances \
    $AMI \
    --key acp-ec2 \
    --user-data-file user_data_app_server.sh \
    --instance-count 1 \
    --group ssh_access \
    --group app_servers \
    --monitor \
    --instance-initiated-shutdown-behavior stop \
    --availability-zone us-east-1b \
    --instance-type c1.medium \
    --block-device-mapping /dev/sdp=$UDATA_SNAPSHOT:1