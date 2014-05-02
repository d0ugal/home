Quickstart for Installing home
==============================

Home currently makes a large number of assumptions. These steps should work
fine if you are using exactly the same setup. If you don't, you are encouraged
to `raise an issue`_ on GitHub where we would be happy to try and help! The
changes to work on other Unix systems will be relatively minor if you are
using the same or similar devices.

.. _raise an issue: https://github.com/d0ugal/home/issues


Assumptions!
------------

- You are running `Raspbian`_ [#]_ on a Raspberry Pi [#]_.
- You have an `RFXCOM RFXtrx 433`_.
- You have a device supported by the Python library `rfxcom`_ (see a list of
  supported devices in the README, devices are being added over time.)

.. _Raspbian: http://www.raspbian.org/
.. _RFXCOM RFXtrx 433: http://www.rfxcom.com/store/Transceivers/12103
.. _rfxcom: https://github.com/d0ugal/python-rfxcom

.. [#] I am running this version: http://downloads.raspberrypi.org/raspbian_latest
.. [#] I'm using a model B board, the SD card doesn't need to be that big.


Setting up the Raspberry Pi
---------------------------

So, you have a fresh Rasbian setup on your Raspberry Pi? Great. You should be
able to use the `bootstrap script`_ in the Home git repository.

A quick sumamry of what it roughly does, to see in more detail, use the source:

1. apt-get update and upgrade.
2. Install git, postgres, python-dev, pip, screen, supervisor and vim packages
   with apt.
3. Upgrade pip with pip :)
4. Install virtualenv, virtualenvwrapper and tox with pip
5. Download, compile and install Python 3.4 under /opt/python3.4
6. Add the virtualenvwrapper source to the bashrc
7. Tell postgres to listen on local host. This is obviously the most dangerous,
   but as this should only be deployed on a private closed network it should be
   fine.


.. _bootstrap script: https://raw.githubusercontent.com/d0ugal/home/master/home/conf/bootstrap.sh


Installing Home
---------------

Now we are setup, we need to create an environment for Home. First we want to
make a Python 3.4 virtualenv. On the pi, run these commands::

    mkvirtualenv home -p /opt/python3.4/bin/python3.4
    pip install home

Now you have the code installed, we need to finish setting up the database.
You can do this like so::

    home db upgrade
    home create_user admin

You can use any username you want and you will be prompted for a password.


Running Home
------------

The best way to do this is via supervisord. To do that, you need to create a
config file called ``/etc/supervisor/conf.d/home.conf`` with the following
contents::

    [program:home-dashboard]
    command = /home/pi/.virtualenvs/home/bin/home dashboard
    user = pi
    autostart = true
    autorestart = true
    stdout_logfile = /var/log/supervisor/home-dashboard.log
    stderr_logfile = /var/log/supervisor/home-dashboard-error.log

    [program:home-collect]
    command = /home/pi/.virtualenvs/home/bin/home collect --device /dev/serial/by-id/...
    user = pi
    autostart = true
    autorestart = true
    stdout_logfile = /var/log/supervisor/home-collect.log
    stderr_logfile = /var/log/supervisor/home-collect-error.log


You will need to replace the path to your serial device to match what is on
your system.

After that, run::

  sudo service supervisor restart
  ps aux | grep home

You should see some output showing two processes running.

.. note::

    If that doesn't appear to work, try restarting supervisor like this::

        sudo service supervisor stop && sudo service supervisor start

    For some reason the restart function wasn't working for me.

If that worked, you should be able to head the IP of your address on port 5000
in your browser (``http://IP:5000/``). You will be asked to login and then you
will see a dashboard.
