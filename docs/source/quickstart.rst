Quickstart for Installing home
==============================

The current version of home makes a number of assumptions, these steps should
work fine if you use exactly the same setup but will probably still work on
other unix based operating systems with relatively small changes.

Assumptions!
------------

- You are running `Raspbian`_ [#]_ on a Raspberry Pi.
- You have an `RFXCOM RFXtrx 433`_.
- You have a device supported by the Python library `rfxcom`_ and home. This
  means you are running and OWL CM160 electricity sensor and/or a Oregon
  Scientific THGN132N Thermo/Hydro Sensor


.. _Raspbian: http://www.raspbian.org/
.. _RFXCOM RFXtrx 433: http://www.rfxcom.com/store/Transceivers/12103
.. _rfxcom: https://github.com/d0ugal/rfxcom

.. [#] I am running this version: http://downloads.raspberrypi.org/raspbian_latest


Setting up the Raspberry Pi
---------------------------

Assuming you have a fresh Raspbian setup that matches the one referenced above
then you should be able to use the `bootstrap script`_ in the home git
repository to perform all the setup required. Since you shouldn't trust me, I
suggest you copy the commands a block at a time rather than download it all
and run it.

A quick sumamry of what it does:

1. apt-get update and upgrade.
2. Install git, postgres, python-dev, pip, screen and vim packages with apt.
3. Upgrade pip with pip :)
4. Install virtualenv, virtualenvwrapper and tox with pip
5. Download, compile and install Python 3.4 under /opt/python3.4
6. Add the virtualenvwrapper source to the bashrc
7. Tell postgres to listen on local host. This is obviously the most dangerous,
   but as this should only be deployed on a private closed network it should be
   fine.


.. _bootstrap script: https://raw.githubusercontent.com/d0ugal/home/master/bootstrap.sh


Installing home
---------------

Ok, first lets make a Python 3.4 virtualenv to run things from. So, after you
SSH into the Pi, follow these commands::

    mkvirtualenv home -p /opt/python3.4/bin/python3.4
    pip install home

Done!

Now you should have some new commands under the name home-*, the first one we
will do will setup the database::

    home-syncdb

If there is no output, it worked. `Ghetto right?`

Now we need to find the rfxtrx, you have it connected to the Pi's USB right?
You'll find the path for it under ``/dev/serial/by-id/`` with my setup it shows
as exactly ``/dev/serial/by-id/usb-RFXCOM_RFXtrx433_A1WYT9NA-if00-port0``

Ok, now we know everything we need.


Running home
------------

- SSH to your pi
- Start a screen session with the command ``screen``
- Activate the virtualenv with ``workon home``
- Run the command ``home-collection --device /dev/serial/by-id/...`` where the
  path is the full path to your serial device.

Assuming this has worked, you will start to see some logged output with home
outputting the packets its receiving and it'll output the value its storing.


Viewing the datas
-----------------

There isn't much support for this yet, but you can run the following command to
get some really basic stuff::

    home-report

Otherwise, connect to postgres with ``psql -U home`` and the password `home`
when it asks for it, then you can explore and find more interesting things.

Find out when we last got data from each device::

    SELECT device.id, device.name, max(data_point.created_at)
    FROM data_point
    JOIN device ON (data_point.device_id = device.id)
    GROUP BY device.id
    ORDER by max;

See how many data points, the max and the min for each device on each recorded
data series::

    SELECT series.name AS series, device.name AS device, count(device.id),
        max(value), min(value), max(data_point.created_at) as latest
    FROM data_point
    JOIN device ON (data_point.device_id = device.id)
    JOIN series ON (data_point.series_id = series.id)
    GROUP BY device.id, series.id
    ORDER BY series.name, max DESC;
