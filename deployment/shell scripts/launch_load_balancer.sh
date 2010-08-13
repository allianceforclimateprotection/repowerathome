#!/bin/bash

# This script launches a new load balancer

# Set this variable to the load balancer AMI
AMI=ami-985ab1f1

# Set this variable to an EBS snapshot containing user data
UDATA_SNAPSHOT=snap-62923409

ec2-run-instances \
    $AMI \
    --key acp-ec2 \
    --user-data-file user_data_load_balancer.sh \
    --instance-count 1 \
    --group ssh_access \
    --group load_balancers \
    --monitor \
    --instance-initiated-shutdown-behavior stop \
    --availability-zone us-east-1b \
    --instance-type m1.small \
    --block-device-mapping /dev/sdp=$UDATA_SNAPSHOT:1