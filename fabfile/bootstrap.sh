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

system_enable_universe
system_update
system_update_locale_en_US_UTF_8
system_set_timezone 'America/New_York'
install_emacs

function install_loadbalancer_libs {
    apt-get -y install libssl-dev memcached nginx
}

function configure_nginx {
    rm /etc/nginx/sites-available/default
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
    ln -s /etc/nginx/sites-available/rah /etc/nginx/sites-enabled/rah
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
}

install_loadbalancer_libs
configure_nginx
install_s3cmd
configure_ssl
configure_htpasswd

function install_appserver_libs {
    apt-get -y install apache2-prefork-dev memcached git-core mercurial default-jre
    apt-get -y install libjpeg62-dev libfreetype6-dev
    apt-get -y install python python-dev python-setuptools
    easy_install pip virtualenv yolk ipython
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

install_appserver_libs
configure_apache2
install_send_messages_cron
install_codebase_keys
init_project