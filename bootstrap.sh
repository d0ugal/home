#!/bin/sh -xe

sudo apt-get -y update && sudo apt-get -y upgrade;
sudo apt-get -y install \
    git-core \
    postgresql \
    postgresql-server-dev-all \
    python-dev \
    python-pip \
    screen \
    vim \
    ;

sudo pip install -IU pip;
sudo pip install -IU virtualenv virtualenvwrapper tox;

if [ ! -f /opt/python3.4/bin/python3 ]; then
    cd /tmp;
    wget https://www.python.org/ftp/python/3.4.0/Python-3.4.0.tgz;
    tar xvzf ./Python-3.4.0.tgz
    cd ./Python-3.4.0
    ./configure --prefix=/opt/python3.4
    make && sudo make install
fi


if ! grep -q virtualenvwrapper ~/.bashrc; then
    echo '
    source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
fi

if ! sudo -u postgres -- psql -c "SELECT usename FROM pg_user;" | grep -iq home; then
    sudo echo "local    all         all         ident
local    all         all         password
host    all         all    127.0.0.1/32     password" > /etc/postgresql/9.1/main/pg_hba.conf
    sudo -u postgres -- psql -c "CREATE ROLE home NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN PASSWORD 'home'";
    sudo -u postgres -- createdb -T template0 -E UTF8 -O home home;
    sudo -u postgres -- createdb -T template0 -E UTF8 -O home test_home;
fi
