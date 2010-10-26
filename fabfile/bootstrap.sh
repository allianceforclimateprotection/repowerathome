#!/bin/bash

set -e -x
export DEBIAN_FRONTEND=noninteractive
export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'

function system_enable_universe {
    sed -i 's/^#\(.*deb.*\) universe/\1 universe/' /etc/apt/sources.list
    sed -i 's/^#\(.*deb.*\) multiverse/\1 multiverse/' /etc/apt/sources.list
}

function system_update {
    apt-get update
    apt-get -y upgrade
}

function system_update_locale_en_US_UTF_8 {
    dpkg-reconfigure locales
    update-locale LANG=en_US.UTF-8
}

function system_set_timezone {
    # $1 - Timezone
    echo $1 > /etc/timezone
    dpkg-reconfigure -f noninteractive tzdata
}

function get_user_home {
    # $1 - username
    cat /etc/passwd | grep "^$1:" | cut -d: -f6
}

function install_emacs {
    apt-get -y install emacs
    USER_HOME=`get_user_home ubuntu`
    sudo -u "ubuntu" touch "$USER_HOME/.emacs"
    sudo -u "ubuntu" echo '(setq backup-directory-alist `(("." . "~/.saves")))' >> "$USER_HOME/.emacs"
}

function mysql_client_install {
    apt-get -y install mysql-client
}

function mysql_server_install {
    # $1 - the mysql root password
    if [ ! -n "$1" ]; then
        echo "mysql_install() requires the root pass as its first argument"
        return 1;
    fi

    echo "mysql-server-5.1 mysql-server/root_password password $1" | debconf-set-selections
    echo "mysql-server-5.1 mysql-server/root_password_again password $1" | debconf-set-selections
    apt-get -y install mysql-server

    echo "Sleeping while MySQL starts up for the first time..."
    sleep 5
}

function mysql_create_database {
    # $1 - the mysql root password
    # $2 - the db name to create
    if [ ! -n "$1" ]; then
        echo "mysql_create_database() requires the root pass as its first argument"
        return 1;
    fi
    if [ ! -n "$2" ]; then
        echo "mysql_create_database() requires the name of the database as the second argument"
        return 1;
    fi
    echo "CREATE DATABASE $2;" | mysql -u root -p$1
}

function mysql_create_user {
    # $1 - the mysql root password
    # $2 - the user to create
    # $3 - their password
    if [ ! -n "$1" ]; then
        echo "mysql_create_user() requires the root pass as its first argument"
        return 1;
    fi
    if [ ! -n "$2" ]; then
        echo "mysql_create_user() requires username as the second argument"
        return 1;
    fi
    if [ ! -n "$3" ]; then
        echo "mysql_create_user() requires a password as the third argument"
        return 1;
    fi
    echo "CREATE USER '$2'@'localhost' IDENTIFIED BY '$3';" | mysql -u root -p$1
}

function mysql_grant_user {
    # $1 - the mysql root password
    # $2 - the user to bestow privileges
    # $3 - the database
    if [ ! -n "$1" ]; then
        echo "mysql_create_user() requires the root pass as its first argument"
        return 1;
    fi
    if [ ! -n "$2" ]; then
        echo "mysql_create_user() requires username as the second argument"
        return 1;
    fi
    if [ ! -n "$3" ]; then
        echo "mysql_create_user() requires a database as the third argument"
        return 1;
    fi
    echo "GRANT ALL PRIVILEGES ON $3.* TO '$2'@'localhost';" | mysql -u root -p$1
    echo "FLUSH PRIVILEGES;" | mysql -u root -p$1
}

function install_appserver_libs {
    apt-get -y install apache2 libapache2-mod-wsgi apache2-prefork-dev memcached git-core mercurial
    apt-get -y install libjpeg62-dev libfreetype6-dev
    apt-get -y install python python-dev python-setuptools
    easy_install pip virtualenv yolk http://pypi.python.org/packages/source/i/ipython/ipython-0.10.1.zip
}

function configure_apache2 {
    rm /etc/apache2/sites-available/default
    rm /etc/apache2/sites-available/default-ssl
    rm /etc/apache2/sites-enabled/000-default
    
    cat > '/etc/apache2/ports.conf' << EOF
::server_config_files/apache2/ports.conf::
EOF
    cat > '/etc/apache2/httpd.conf' << EOF
::server_config_files/apache2/httpd.conf::
EOF
    cat > '/etc/apache2/sites-available/rah' << EOF
::server_config_files/apache2/rah::
EOF

    sed -i "s/_public_dns_name/`echo $PUBLIC_DNS_NAME`/" /etc/apache2/sites-available/*
    ln -s /etc/apache2/sites-available/rah /etc/apache2/sites-enabled/rah
}

function install_send_messages_cron {
    cat > '/etc/cron.d/send_read_messages' << EOF
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin:/usr/local/sbin
MAILTO="cron@repowerathome.com"
HOME=/home/ubuntu

*/15 * * * * ubuntu /home/ubuntu/webapp/manage.py send_ready_messages >> /home/ubuntu/send_ready_messages.log 2>&1
EOF
}

function install_s3cmd {
    apt-get -y install s3cmd
    cat > s3cmd_input << EOF
`echo $AWS_ACCESS_KEY`
`echo $AWS_SECRET_KEY`


Yes
Y
Y
Y
EOF
    s3cmd --configure < s3cmd_input
    rm s3cmd_input
}

function install_codebase_keys {
    USER_HOME=`get_user_home ubuntu`
    sudo -u "ubuntu" touch "$USER_HOME/.ssh/config"
    sudo -u "ubuntu" cat > "$USER_HOME/.ssh/config" << EOF
Host codebasehq.com
  HostName codebasehq.com
  User git
  IdentityFile /home/ubuntu/.ssh/deploy-pk.pem
  StrictHostKeyChecking no
EOF
    s3cmd get --force s3://private.repowerathome.com/codebase/deploy.pem "$USER_HOME/.ssh/deploy.pem"
    s3cmd get --force s3://private.repowerathome.com/codebase/deploy-pk.pem "$USER_HOME/.ssh/deploy-pk.pem"
    chmod 0400 "$USER_HOME/.ssh/deploy.pem" "$USER_HOME/.ssh/deploy-pk.pem"
    chown ubuntu:ubuntu "$USER_HOME/.ssh/deploy.pem" "$USER_HOME/.ssh/deploy-pk.pem"
}

function init_project {
    USER_HOME=`get_user_home ubuntu`
    sudo -u "ubuntu" git clone git@codebasehq.com:rah/rah/rah.git "$USER_HOME/webapp/"
    sudo -u "ubuntu" mkdir "$USER_HOME/requirements/"
}

function s3_key_replacement {
    # $1 - key to download
    # $2 - file to replace in
    # $3 - string to replace
    KEY_NAME="$1"
    FILE="$2"
    PATTERN="$3"
    s3cmd get --force "s3://private.repowerathome.com/$KEY_NAME" temp_key
    sed -i 's/[\&]/\\&/g' temp_key # escape any special chars in the key
    sed -i "s/$PATTERN/`cat temp_key`/g" "$FILE"
    rm temp_key
}

function install_local_settings {
    USER_HOME=`get_user_home ubuntu`
    sudo -u "ubuntu" touch "$USER_HOME/webapp/local_settings.py"
    sudo -u "ubuntu" cat > "$USER_HOME/webapp/local_settings.py" << EOF
DEBUG = False
TEMPLATE_DEBUG = DEBUG
SEND_BROKEN_LINK_EMAILS = not DEBUG
IGNORABLE_404_ENDS = ("ga.js/", "b.js/",)

INTERNAL_IPS = ("127.0.0.1", "157.130.44.166")

ADMINS = (
    ('Server Errors', 'servererrors@repowerathome.com'),
)
MANAGERS = ADMINS

DATABASE_ENGINE   = 'mysql'
DATABASE_NAME     = 'rah'
DATABASE_USER     = 'rah_db_user'
DATABASE_PASSWORD = "$DB_PASSWORD"
DATABASE_HOST     = "$DB_HOST"
DATABASE_PORT     = "$DB_PORT"

# Email Settings
EMAIL_HOST = "localhost"
DEFAULT_FROM_EMAIL = "Repower at Home <noreply@repowerathome.com>"
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_API_KEY = '_postmark_api_key'

MEDIA_URL = 'http://_s3_bucket_name/'
MEDIA_URL_HTTPS = 'https://s3.amazonaws.com/_s3_bucket_name/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Secrets and Keys
SECRET_KEY = '_secret_key'
AWS_BUCKET_NAME = '_s3_bucket_name'
AWS_STORAGE_BUCKET_NAME = AWS_BUCKET_NAME
AWS_ACCESS_KEY_ID = "$AWS_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "$AWS_SECRET_KEY"
TWITTER_CONSUMER_KEY = '_twitter_consumer_key'
TWITTER_CONSUMER_SECRET = '_twitter_consumer_secret'
FACEBOOK_APPID = '_facebook_appid'
FACEBOOK_SECRET = '_facebook_secret'
EOF
    sed -i "s/_s3_bucket_name/`echo $ENVIRONMENT`.static.repowerathome.com/" "$USER_HOME/webapp/local_settings.py"

    s3_key_replacement "django/secret_key" "$USER_HOME/webapp/local_settings.py" "_secret_key"
    s3_key_replacement "django/postmark_api_key" "$USER_HOME/webapp/local_settings.py" "_postmark_api_key"
    s3_key_replacement "django/$ENVIRONMENT/twitter_consumer_key" "$USER_HOME/webapp/local_settings.py" "_twitter_consumer_key"
    s3_key_replacement "django/$ENVIRONMENT/twitter_consumer_secret" "$USER_HOME/webapp/local_settings.py" "_twitter_consumer_secret"
    s3_key_replacement "django/$ENVIRONMENT/facebook_appid" "$USER_HOME/webapp/local_settings.py" "_facebook_appid"
    s3_key_replacement "django/$ENVIRONMENT/facebook_secret" "$USER_HOME/webapp/local_settings.py" "_facebook_secret"
}

function install_loadbalancer_libs {
    apt-get -y install libssl-dev memcached nginx
}

function configure_nginx {
    rm /etc/nginx/sites-available/default
    rm /etc/nginx/sites-enabled/default
    
    cat > '/etc/nginx/nginx.conf' << EOF
::server_config_files/nginx/nginx.conf::
EOF
    cat > '/etc/nginx/sites-available/maintenance' << EOF
::server_config_files/nginx/maintenance::
EOF
    cat > '/etc/nginx/sites-available/maintenance_base' << EOF
::server_config_files/nginx/maintenance_base::
EOF
    cat > '/etc/nginx/sites-available/maintenance_ssl' << EOF
::server_config_files/nginx/maintenance_ssl::
EOF
    cat > '/etc/nginx/sites-available/rah' << EOF
::server_config_files/nginx/rah::
EOF
    cat > '/etc/nginx/sites-available/rah_base' << EOF
::server_config_files/nginx/rah_base::
EOF
    cat > '/etc/nginx/sites-available/rah_base_http' << EOF
::server_config_files/nginx/rah_base_http::
EOF
    cat > '/etc/nginx/sites-available/rah_base_https' << EOF
::server_config_files/nginx/rah_base_https::
EOF
    
    sed -i "s/_public_dns_name/`echo $PUBLIC_DNS_NAME`/" /etc/nginx/sites-available/*
    APPSERVER_ADDRESSES=""
    for server in $APP_SERVER_IPS
    do
        APPSERVER_ADDRESSES="$APPSERVER_ADDRESSES server $server:8080;"
    done
    sed -i "s/_upstream_servers/`echo $APPSERVER_ADDRESSES`/" /etc/nginx/sites-available/*
    ln -s /etc/nginx/sites-available/rah /etc/nginx/sites-enabled/rah
}

function configure_ssl {
    s3cmd get --force s3://private.repowerathome.com/ssl/repowerathome.key /etc/ssl/repowerathome.key
    s3cmd get --force s3://private.repowerathome.com/ssl/repowerathome.csr /etc/ssl/private/repowerathome.csr
    s3cmd get --force s3://private.repowerathome.com/ssl/repowerathome.key /etc/ssl/private/repowerathome.key
    s3cmd get --force s3://private.repowerathome.com/ssl/repowerathome_with_pass.key /etc/ssl/private/repowerathome_with_pass.key
    s3cmd get --force s3://private.repowerathome.com/ssl/repowerathome.crt /etc/ssl/certs/repowerathome.crt
    s3cmd get --force s3://private.repowerathome.com/ssl/repowerathome_with_gd_bundle.crt /etc/ssl/certs/repowerathome_with_gd_bundle.crt
}

function configure_htpasswd {
    USER_HOME=`get_user_home ubuntu`
    s3cmd get s3://private.repowerathome.com/htpasswd "$USER_HOME/htpasswd"
    chown ubuntu:ubuntu "$USER_HOME/htpasswd"
}

function bootstrap_system {
    system_enable_universe
    system_update
    system_update_locale_en_US_UTF_8
    system_set_timezone 'America/New_York'
    install_emacs
}

function bootstrap_database {
    mysql_client_install
    mysql_server_install "$DB_PASSWORD"
    mysql_create_database "$DB_PASSWORD" "$DB_NAME"
    mysql_create_user "$DB_PASSWORD" "$DB_USER" "$DB_PASSWORD"
    mysql_grant_user "$DB_PASSWORD" "$DB_USER" "$DB_NAME"
}

function bootstrap_appserver {
    install_appserver_libs
    configure_apache2
    mysql_client_install
    install_send_messages_cron
    install_s3cmd
    install_codebase_keys
    init_project
    install_local_settings
    /etc/init.d/apache2 restart
}

function bootstrap_loadbalancer {
    install_loadbalancer_libs
    configure_nginx
    install_s3cmd
    configure_ssl
    configure_htpasswd
    /etc/init.d/nginx restart
}