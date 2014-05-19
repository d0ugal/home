#!/bin/sh -xe

sudo apt-get -y update && sudo apt-get -y upgrade;

sudo apt-get -y install \
    git-core \
    nginx \
    python-dev \
    python-pip \
    redis-server \
    screen \
    supervisor \
    vim \
    ;

# Upgrade pip, the packaged version can be pretty old.
sudo pip install -IU pip;

# Install everything we need for managing virtualenvs
sudo pip install -IU virtualenv virtualenvwrapper tox;

# Install postgres client, server and contrib (for hstore)
sudo apt-get -y install \
    postgresql \
    postgresql-contrib-9.1 \
    postgresql-server-dev-all \
    ;

# Setup postgres to allow password login from localhost and create a home user
# and database for test and production.
if ! sudo -u postgres -- psql -c "SELECT usename FROM pg_user;" | grep -iq home; then
    sudo echo "local    all         all         ident
local    all         all         password
host    all         all    127.0.0.1/32     password" > /etc/postgresql/9.1/main/pg_hba.conf
    sudo -u postgres -- psql -c "CREATE ROLE home NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN PASSWORD 'home'";
    sudo -u postgres -- createdb -T template0 -E UTF8 -O home home;
    sudo -u postgres -- createdb -T template0 -E UTF8 -O home test_home;
    sudo -u postgres -- psql -c "CREATE EXTENSION hstore" home;
    sudo -u postgres -- psql -c "CREATE EXTENSION hstore" test_home;
fi

# There are few good options for Python 3.4 packages, so, download and install
# from source. Installing with a prefix under /opt/ so it doesn't touch the
# system Python and isn't on our path by default.
if [ ! -f /opt/python3.4/bin/python3 ]; then
    cd /tmp;
    wget https://www.python.org/ftp/python/3.4.0/Python-3.4.0.tgz;
    tar xvzf ./Python-3.4.0.tgz
    cd ./Python-3.4.0
    ./configure --prefix=/opt/python3.4
    make && sudo make install
fi

# Add the virtualenv wrapper hooks to our bashrc.
if ! grep -q virtualenvwrapper ~/.bashrc; then
    echo '
    source /usr/local/bin/virtualenvwrapper_lazy.sh' >> ~/.bashrc
fi

id -u pi &>/dev/null || useradd pi;


if [ ! -d /var/log/home ]; then
    sudo mkdir /var/log/home;
    sudo chown pi /var/log/home;
fi
