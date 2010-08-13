#!/bin/bash

# This must be unique for every RDS instance
DB_IDENTIFIER="testing"

rds-create-db-instance $DB_IDENTIFIER \
    --preferred-backup-window 08:00-10:00 \
    --preferred-maintenance-window Sun:10:00-Sun:14:00 \
    --db-parameter-group-name rah \
    --master-username rah_db_user \
    --master-user-password - \
    --availability-zone us-east-1b \
    --engine mysql5.1 \
    --db-name rah_master \
    --db-instance-class db.m1.small \
    --db-security-groups default \
    --multi-az false \
    --port 3306 \
    --backup-retention-period 7 \
    --allocated-storage 5